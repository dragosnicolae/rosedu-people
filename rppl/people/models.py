import os.path
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime

class Person(User):
    description = models.TextField(max_length=2000, blank=True)
    organisations = models.ManyToManyField('Organization',  blank=True, null=True, related_name="persons")

    @property
    def person_roles(self):
        return PersonRole.objects.filter(person=self).order_by('edition')

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __unicode__(self):
        return self.name


class Link(models.Model):
    """ Link for person's external accounts """
    url = models.CharField(max_length=100)
    person = models.ForeignKey(Person, blank=True, null=True)

    def __unicode__(self):
        return self.url


class Organization(models.Model):
    """ External affiliations for users """
    url = models.CharField(max_length=100)

    def __unicode__(self):
        return self.url


class Project(models.Model):
    """ Project in community """
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    logo = models.ImageField(blank=True, null=True, upload_to=settings.MEDIA_ROOT)

    def __unicode__(self):
        return self.name

    def logo_url(self):
        return "/resources/upload/" + os.path.basename(self.logo.url) if self.logo else ''

    @property
    def editions(self):
        return Edition.objects.filter(project=self).order_by('-date_end')


class Edition(models.Model):
    """ Project edition """
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=100)
    picture = models.ImageField(blank=True, null=True, upload_to=settings.MEDIA_ROOT)

    date_start = models.DateField(default=datetime.now)
    date_end = models.DateField(default=datetime.now)
    persons = models.ManyToManyField(Person, through='PersonRole', blank=True)

    @property
    def person_roles(self):
        return PersonRole.objects.filter(edition=self).order_by('role')

    def picture_url(self):
        return "/resources/upload/" + os.path.basename(self.picture.url) if self.picture else ''

    def __unicode__(self):
        return self.name


class Role(models.Model):
    """ A role that can be given to many persons in an edition """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class PersonRole(models.Model):
    person = models.ForeignKey(Person)
    edition = models.ForeignKey(Edition)
    role = models.ForeignKey(Role)
    timestamp = models.DateTimeField(default=datetime.now)
