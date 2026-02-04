from core.models import User


class FakeUserFactory:
    """Fake User Factory for testing purposes"""

    def create_superuser(self, **kwargs):
        email = kwargs.pop("email", None)
        password = kwargs.pop("password", None)
        return User.objects.create_superuser(email, password, **kwargs)

    def create_user(self, **kwargs):
        email = kwargs.pop("email", None)
        password = kwargs.pop("password", None)
        return User.objects.create_user(email, password, **kwargs)

    def create_user_with_reduced_kwargs(self, reduced_fields=[]):
        reduced_kwargs = self._get_user_kwargs(
            reduced=True, reduced_fields=reduced_fields
        )
        return self.create_user(**reduced_kwargs)

    def _get_user_kwargs(self, reduced=False, reduced_fields=[]):
        user_kwargs = {
            "email": "testuser@example.com",
            "password": "testpass123",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
        }
        if reduced:
            for field in reduced_fields:
                user_kwargs.pop(field, None)
        return user_kwargs

    @staticmethod
    def get_all_user_fields():
        return [
            "logentry",
            "sent_requests",
            "received_requests",
            "connections_left",
            "connections_right",
            "blocks_created",
            "blocks_received",
            "owned_servers",
            "role",
            "sent_invites",
            "members",
            "messages",
            "id",
            "password",
            "last_login",
            "is_superuser",
            "uid",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "status",
            "created_at",
            "updated_at",
            "is_staff",
            "is_deleted",
            "is_verified",
            "profile_pic",
            "banner",
            "metadata",
            "server_data",
            "groups",
            "user_permissions",
        ]
