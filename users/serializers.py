from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
# from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator
from .models import User, Profile
from master.models import Vehicle


class UserSerializer(serializers.ModelSerializer):
    # vehicle = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='vehicle-detail')
    profile = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='profile-detail')

    class Meta:
        model = User
        read_only_fields = ('id')
        fields = ('id', 'email', 'username', 'phone_number', 'first_name', 'last_name', 'profile')
        # fields = ('id', 'email', 'username', 'phone_number', 'first_name', 'last_name', 'profile', 'vehicle')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # vehicle_id = serializers.SerializerMethodField(read_only=True)
    # vehicle_registration_number = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'gender', 'dob', 'bio', 'image']
        # fields = ['user', 'gender', 'dob', 'bio', 'vehicle_id', 'vehicle_registration_number', 'image', 'user_registration_number']

    # def get_vehicle_id(self, obj):
    #     return Vehicle.objects.all().filter(users=obj.user.id)[0].id

    # def get_vehicle_registration_number(self, obj):
    #     return Vehicle.objects.all().filter(users=obj.user.id)[0].registration_number


class CustomRegisterSerializer(RegisterSerializer):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = serializers.CharField(validators=[phone_regex], max_length=17, allow_blank=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'phone_number')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'phone_number': self.validated_data.get('phone_number', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        adapter.save_user(request, user, self)
        return user

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
