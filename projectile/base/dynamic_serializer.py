from rest_framework import serializers

from core.models import User
from server.models import (
    Server,
    Category,
    Channel,
    Thread,
    Role,
    RolePermission,
    Invite,
)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserDynamicSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ServerDynamicSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Server
        fields = "__all__"


class CategoryDynamicSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ChannelDynamicSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"


class ThreadDynamicSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"


class RoleDynamicSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class RolePermissionDynamicSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = RolePermission
        fields = "__all__"


class InviteDynamicSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Invite
        fields = "__all__"
