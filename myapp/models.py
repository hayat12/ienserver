from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from myapp import helper
from myapp import constants


def ien_media(instance, filename):
    return instance.get_upload_path(filename) #'__{0}__/{1}'.format(instance.id, filename)

class UserProfile(models.Model):

    class Meta:
        db_table = 'ien_user'

    picture = models.ImageField(
        max_length=255, blank=True, null=True, upload_to=constants.MEDIA_PATH.USER_PP_PATH)
    company_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=254, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='user')

    steps = models.IntegerField(null=True, default=0)
    designation = models.CharField(max_length=250, null=True)
    about_me = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    dob = models.CharField(max_length=50, null=True, blank=True)
    # address = models.TextField(blank=True, null=True)
    organization_name = models.CharField(blank=True, null=True, max_length=250)
    position_held = models.CharField(blank=True, null=True, max_length=250)
    passport = models.CharField(blank=True, null=True, max_length=250)
    account_no = models.CharField(blank=True, null=True, max_length=250)
    bank_name = models.CharField(null=True, blank=True, max_length=250)
    main_interest = models.CharField(max_length=250, null=True, blank=True)
    sub_interest = models.CharField(max_length=250, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='created_by')
    modified_date = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='+', db_column='modified_by')

    # def get_upload_path(self, filename):
    #     o = constants.MEDIA_PATH.USER_PP_PATH
    #     return str(o)+str(self.user.id)+"/"+filename


class Event(models.Model):
    class Meta:
        verbose_name = "Event"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='user')
    event_name = models.CharField(max_length=250, null=True, blank=True)
    category = models.CharField(max_length=250, null=True, blank=True)
    location = models.TextField(blank=True, null=True)
    selected_address = models.TextField(blank=True, null=True)
    about_event = models.TextField(blank=True, null=True)
    event_image = models.ImageField(blank=True, null=True, upload_to=constants.MEDIA_PATH.EVEN_MEDIA_PATH)
    start_time = models.TextField(blank=False, null=False)
    start_date = models.DateField(blank=False, null=False)
    end_time = models.TextField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='created_by')
    modified_date = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='+', db_column='modified_by')


class Connection(models.Model):
    class Meta:
        verbose_name = "Connection"
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='user')
    invited_id = models.IntegerField(blank=False, null=False)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='+', db_column='modified_by')


class Adgenda(models.Model):
    class Meta:
        verbose_name = "Adgenda"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='user')
    title = models.CharField(max_length=250, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=False, null=False)
    start_date = models.DateField(blank=False, null=False)

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='created_by')
    modified_date = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='+', db_column='modified_by')


class MarketPlace(models.Model):
    class Meta:
        verbose_name = "market_place"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='user')
    item_name = models.CharField(max_length=250, null=True, blank=True)
    price = models.CharField(max_length=250, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    picture = models.ImageField(
        max_length=255, blank=True, null=True, upload_to='media')

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='created_by')
    modified_date = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='+', db_column='modified_by')


class AdgendaInvites(models.Model):
    class Meta:
        verbose_name = "AdgendaInvites"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='user'),
    # invite_id = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='invite_id')
    invite_id = models.IntegerField(blank=False, null=False)
    status = models.IntegerField(blank=True, null=True)
    adg_id = models.IntegerField(blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='created_by')
    modified_date = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='+', db_column='modified_by')


class EventInvites(models.Model):
    class Meta:
        verbose_name = "event_invites"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='user'),
    invite_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='invite_id')
    # invite_id is invited user id
    status = models.IntegerField(blank=True, null=True)
    event_id = models.IntegerField(blank=False, null=False)

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='created_by')
    modified_date = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='+', db_column='modified_by')

class EventPicture(models.Model):
    class Meta:
        verbose_name = "event_picture"
    event_id = models.ForeignKey(Event, on_delete=True)
    picture = models.ImageField(blank=True, null=True, upload_to=constants.MEDIA_PATH.EVEN_MEDIA_PATH)

class MarketPlacePictures(models.Model):
    class Meta:
        verbose_name = "market_place_picture"
    market_place_id = models.ForeignKey(MarketPlace, on_delete=True)
    picture = models.ImageField(blank=True, null=True, upload_to=constants.MEDIA_PATH.MARKET_PLACE_MEDIA_PATH)

class UploadIMG(models.Model):
    picture = models.ImageField(blank=True, null=True, upload_to=ien_media)
    def save(self, force_insert=False, force_upload=False, using=None):
        super(UploadIMG, self).save()
