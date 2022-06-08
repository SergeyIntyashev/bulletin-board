import uuid

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class User(AbstractUser):
    """User model"""
    ROLES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]
    STATUS_LIST = [
        ('blocked', 'blocked'),
        ('active', 'active'),
        ('unactivated', 'unactivated'),
    ]

    username = models.CharField('name', max_length=255)
    firstname = models.CharField('name', max_length=255)
    lastname = models.CharField('last name', max_length=255)
    middlename = models.CharField('middle name', max_length=255, blank=True)
    role = models.CharField('role', max_length=9, choices=ROLES, default='user')
    email = models.EmailField('email', unique=True)
    phone = PhoneNumberField()
    info = models.CharField('time to call', max_length=3000)
    status = models.CharField('status', max_length=20, choices=STATUS_LIST, default='active')
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Region(models.Model):
    """RegionDirectory model"""

    title = models.CharField('title', max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class City(models.Model):
    """City model"""

    title = models.CharField('title', max_length=255)
    slug = models.SlugField(unique=True),
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='region'
    )
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Announcement(models.Model):
    """Announcement model"""

    STATUS_LIST = [
        ('draft', 'draft'),
        ('on_moderation', 'on_moderation'),
        ('rejected', 'rejected'),
        ('archive', 'archive'),
        ('active', 'active'),
    ]

    uuid = models.UUIDField('uuid', default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField('title', max_length=500)
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        verbose_name='category'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name='city'
    )
    price = models.DecimalField('price', max_digits=9, decimal_places=2)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='owner'
    )
    views = models.PositiveIntegerField('views', default=0)
    status = models.CharField('status', max_length=20, choices=STATUS_LIST, default='draft')
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    def __str__(self):
        return f'uuid: {self.uuid} owner email: {self.owner.email} status: {self.status}'

    class Meta:
        ordering = ['-created_at']


def announcement_directory_path(instance, filename):
    return 'announcements/announcement_{0}/{1}'.format(instance.announcement.uuid, filename)


class Category(models.Model):
    """Category model"""

    title = models.CharField('title', max_length=255, blank=False)
    description = models.CharField('description', max_length=5000, blank=True)
    slug = models.SlugField(unique=True),
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Image(models.Model):
    """Image model"""

    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=announcement_directory_path, null=True, blank=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    def __str__(self):
        return f'id: {self.id} announcement: {self.announcement.uuid}'

