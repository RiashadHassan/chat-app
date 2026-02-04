import time

from django.test import TestCase
from django.db import transaction, IntegrityError

from core.models import User
from core.tests.helpers import FakeUserFactory


class UserModelTest(TestCase):
    def setUp(self):
        super().setUp()
        self._factory = FakeUserFactory()
        self.all_user_fields = FakeUserFactory.get_all_user_fields()
        self.static_user_kwargs = self._factory._get_user_kwargs()

    def test_create_user_success(self):
        user = self._factory.create_user(**self.static_user_kwargs)
        self.assertIsInstance(user, User)

    def test_create_user_missing_email(self):
        with self.assertRaises(ValueError) as context:
            self._factory.create_user_with_reduced_kwargs(reduced_fields=["email"])
        self.assertEqual(str(context.exception), "An Email Must Be Provided!")

    def test_create_user_missing_password(self):
        with self.assertRaises(ValueError) as context:
            self._factory.create_user_with_reduced_kwargs(reduced_fields=["password"])
        self.assertEqual(str(context.exception), "A Password Must Be Provided!")

    def test_create_superuser_success(self):
        # if no exception is raised, the test passes
        superuser = self._factory.create_superuser(**self.static_user_kwargs)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_user_model_fields(self):
        user = self._factory.create_user(**self.static_user_kwargs)
        user_fields = [field.name for field in user._meta.get_fields()]
        print(user_fields)
        self.assertCountEqual(user_fields, self.all_user_fields)

    def test_user_str_representation(self):
        user = self._factory.create_user(**self.static_user_kwargs)
        self.assertEqual(str(user), f"{user.username} : {user.email}")

    def test_user_updated_at_on_save(self):
        user = self._factory.create_user(**self.static_user_kwargs)
        original_updated_at = user.updated_at
        # sleep to ensure timestamp difference
        # longer sleeps slow down tests, so we keep it minimal
        time.sleep(0.01)
        user.first_name = "Updated Name"
        user.save()
        self.assertGreater(user.updated_at, original_updated_at)

    def test_not_null_fields(self):
        user = self._factory.create_user(**self.static_user_kwargs)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_unique_fields(self):
        self._factory.create_user(**self.static_user_kwargs)
        with self.assertRaises(IntegrityError):
            self._factory.create_user(**self.static_user_kwargs)

    def test_is_deleted_default(self):
        user = self._factory.create_user(**self.static_user_kwargs)
        self.assertFalse(user.is_deleted)

    def test_metadata_field_default(self):
        user = self._factory.create_user(**self.static_user_kwargs)
        self.assertEqual(user.metadata, {})

    def test_not_null_constraints(self):
        # test only custom model fields that should not be null
        non_nullable_fields = ["email", "username", "first_name", "last_name"]

        for field in non_nullable_fields:
            with self.subTest(field=field):
                # create a fresh user for each test to avoid state issues
                test_user = self._factory.create_user(**self.static_user_kwargs)
                # updating non-nullable fields to 'None' should raise IntegrityError
                try:
                    # wrap in transaction to avoid TransactionManagementError
                    # in 'django.test.TestCase', simpler than a separate 'TransactionTestCase'
                    with transaction.atomic():
                        setattr(test_user, field, None)
                        test_user.save()
                except IntegrityError as e:
                    pass

                test_user.refresh_from_db()
                self.assertIsNotNone(getattr(test_user, field))
                test_user.delete()
