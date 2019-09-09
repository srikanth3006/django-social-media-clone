from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse

from django import template
register = template.Library()
User = get_user_model()
# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name',]

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_groups')

    def __str__(self):
        return self.username

    class Meta:
        unique_together = ['group', 'user']