from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from cloudinary.models import CloudinaryField

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Additional fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = CloudinaryField('image', folder='profile_images', blank=True, null=True, default=None)

    # Override default fields
    email =   models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    class Meta:
        permissions = (
                        ("can_add_staff", "To add staff"),
                        ("can_edit_staff", "To edit staff"),
                        ("can_make_group", "To make group")
                        )
                    