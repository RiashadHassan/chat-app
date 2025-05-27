from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from projectile.server.models import Server, Invite
from projectile.server.utils import generate_invite_code

from projectile.member.models import Member

from ..serializers.invite import InviteListCreateSerializer


class InviteListCreateView(ListCreateAPIView):
    permission_classes = [
        IsAuthenticated
    ]  # TODO: need to add IsMember permission class
    serializer_class = InviteListCreateSerializer

    def get_queryset(self):
        return Invite.objects.filter(
            is_deleted=False,
            expires_at__gt=timezone.now(),
            server_uid=self.kwargs.get("server_uid"),
        )

    def create(self, request, *args, **kwargs):
        try:
            server = get_object_or_404(Server, uid=self.kwargs.get("server_uid"))
            code = generate_invite_code(server.slug)
            invitation = Invite.objects.create(
                server=server, inviter=request.user, code=code
            )
            return Response(
                {"invitation_code": invitation.code}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            # TODO: log the error
            raise exceptions.APIException(detail="Failed to create invitation.")


class AcceptInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        code = self.kwargs.get("code")
        invite = get_object_or_404(Invite, code=code)

        if not invite.is_valid:
            return Response(
                {"detail": "Invite is invalid or expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # prevent duplicate membership
        member, created = Member.objects.get_or_create(
            server=invite.server, user=request.user
        )
        if not created and not member.is_deleted:
            return Response(
                {"detail": "Already a member."}, status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            if member.is_deleted:
                member.is_deleted = False
                member.save()
            invite.uses += 1
            invite.save()

        return Response(
            {"detail": "success", "server": invite.server_uid},
            status=status.HTTP_200_OK,
        )
