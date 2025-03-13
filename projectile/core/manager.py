from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("An Email Must Be Provided!")

        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_superuser", True)
        
        # because is_staff is set to default=True
        kwargs["is_staff"]=True

        if not kwargs.get("is_superuser", False):
            raise ValueError("is_superuser value must be set to True")

        self.create_user(email, password, **kwargs)