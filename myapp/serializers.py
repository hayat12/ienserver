

from django.contrib.auth.models import User
from rest_framework import serializers

from django.contrib.auth.models import User
from .models import UserProfile, Event, Connection, Adgenda, MarketPlace, UploadIMG
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'is_active', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'email', 
            'phone', 
            'picture',
            'company_name',
            'fax',
            'steps',
            'designation',
            'about_me',
            'address',
            'dob',
            'organization_name',
            'position_held',
            'passport',
            'account_no',
            'main_interest',
            'sub_interest'
            )

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'category',
            'about_event',
            'event_name',
            'event_image',
            'selected_address',
            'start_time',
            'start_date',
            'end_time',
            'end_date',
            'location')

class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        ields = (
            'pk',
            'user',
            'picture'
        )

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'created_by',
            'category',
            'about_event',
            'end_time',
            'event_name',
            'event_image',
            'selected_address',
            'start_time',
            'start_date',
            'location',
            'user'
        )

UserModel = get_user_model()
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "username", "password", )

class CreateConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = [
            'user',
            'invited_id',
            'created_by'
        ]
class AdgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adgenda
        fields = [
            'id',
            'title',
            'address',
            'notes',
            'start_date',
            'start_time'
        ]
class MarketPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPlace
        fields = [
            'id',
            'picture',
            'item_name',
            'price',
            'qty',
            'desc'
        ]

class UploadFileSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = MarketPlace
        fields = (
            'user',
            'picture'
        )     
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadIMG
        fields = (
            'pk',
            'picture'
        )