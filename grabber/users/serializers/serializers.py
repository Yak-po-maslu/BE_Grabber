from rest_framework import serializers

from .social_get import SocialLinkSerializer
from ..models import SocialLink
from ..views import CustomUser
import re

User = CustomUser

class UserEditProfileSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(read_only=False, many=True)
    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name','phone_number','show_phone','role', 'date_joined', 'location',
                  'user_photo', 'social_links', 'description']
        extra_kwargs = {
            'email': {'required': True},
        }
        read_only_fields = ['role', 'date_joined', 'id']

    def validate_show_phone(self, value):
        if value in [True, False]:
            return value
        else:
            raise serializers.ValidationError("True or False in field show_phone")

    def validate_phone_number(self, value):

        value = value.strip()

        # Проверка формата: начинается с +, дальше только цифры
        if not re.fullmatch(r'\+380\d{9}', value):
            raise serializers.ValidationError(
                "Phone number must be in format +380XXXXXXXXX (12 digits after +380, no spaces or symbols)."
            )

        return value

    def validate_email(self, value):
        value = value.strip().lower()  # нормалізація email
        user = self.instance

        if user:
            if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use.")
        else:
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_first_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("First name cannot be empty.")
        return value

    def validate_last_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Last name cannot be empty.")
        return value

    def validate_location(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Location cannot be empty.")
        return value.title()

    def update(self, instance, validated_data):
        # забираем social_links из данных
        social_links_data = validated_data.pop('social_links', None)

        # обновляем простые поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # если social_links не передали — ничего не делаем с ними
        if social_links_data is None:
            return instance

        # пересоздаём соцсети
        instance.social_links.all().delete()
        for link_data in social_links_data:
            SocialLink.objects.create(user=instance, **link_data)

        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    social_links = SocialLinkSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name','phone_number','show_phone','role', 'date_joined',
                  'location','user_photo', 'social_links', 'description']
        extra_kwargs = {
            'email': {'required': True},
        }
        read_only_fields = ['role', 'date_joined', 'id']

    def get_phone_number(self, obj):
        # Показуємо номер в любому випадку
        return obj.phone_number




class UserLoginSerializer(serializers.Serializer):
    social_links = SocialLinkSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['email','password']
        extra_kwargs = {
            'email': {'required': True},
        }
        #read_only_fields = ['role', 'date_joined', 'id']
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        value = value.strip().lower()
        if not value:
            raise serializers.ValidationError("Email cannot be empty.")
        return value

    def validate_password(self, value):
        if not value.strip():
            raise serializers.ValidationError("Password cannot be empty.")
        return value



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    email = serializers.EmailField(required=True)
    #first_name = serializers.CharField(required=True)
    #last_name = serializers.CharField(required=True)
    #phone_number = serializers.CharField(required=True)
    #social_links = SocialLinkSerializer(many=True)
    # role = serializers.ChoiceField(
    #     choices=[
    #         (User.Roles.BUYER, "Покупець"),
    #         (User.Roles.SELLER, "Продавець"),
    #     ],
    #     required=False,
    #     default=User.Roles.SELLER
    # )

    class Meta:
        model = User
        fields = ['email','password']

    def validate_email(self, value):
        value = value.strip().lower()
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    # def validate_first_name(self, value):
    #     if not value.strip():
    #         raise serializers.ValidationError("First name cannot be empty.")
    #     return value

    # def validate_last_name(self, value):
    #     if not value.strip():
    #         raise serializers.ValidationError("Last name cannot be empty.")
    #     return value

    # def validate_phone_number(self, value):

    #     value = value.strip()

    #     # Проверка формата: начинается с +, дальше только цифры
    #     if not re.fullmatch(r'\+380\d{9}', value):
    #         raise serializers.ValidationError(
    #             "Phone number must be in format +380XXXXXXXXX (12 digits after +380, no spaces or symbols)."
    #         )

    #     return value

    def validate_password(self, value):
        errors = []

        # 1. Минимальная and max длина
        if len(value) < 6:
            errors.append("Password must be at least 6 characters long.")

        if len(value) > 255:
            errors.append("Password must be at most 255 characters long.")

        # 2. Заглавная буква
        if not re.search(r'[A-Z]', value):
            errors.append("Password must contain at least one uppercase letter.")

        # 3. Строчная буква
        if not re.search(r'[a-z]', value):
            errors.append("Password must contain at least one lowercase letter.")

        # 4. Цифра
        if not re.search(r'[0-9]', value):
            errors.append("Password must contain at least one digit.")

        # 5. Хотя бы один спецсимвол
        special_symbols_pattern = r'[!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?]'
        if not re.search(special_symbols_pattern, value):
                errors.append(f"Password must contain at least one special character: {special_symbols_pattern}")

        allowed = r'^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?]+$'

        # 6. Только латинские символы и спецсимволы
        if not re.fullmatch(allowed, value):
            errors.append(
                "Password may contain only Latin letters, digits and the following special characters: !@#$%^&*()_+-=[]{};':\"\\|,.<>/?"
            )

        if errors:
            raise serializers.ValidationError(errors)

        return value
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)  # 🔐 захешуємо пароль
        user.save()
        return user

    # def validate_role(self, value):
    #     forbidden_roles = ['admin', 'moderator']
    #     if value in forbidden_roles:
    #         raise serializers.ValidationError("You cannot assign this role.")
    #     return value


    # def create(self, validated_data):
    #     social_links_data = validated_data.pop('social_links', [])
    #     user = CustomUser.objects.create(**validated_data)
    #     for link_data in social_links_data:
    #         SocialLink.objects.create(user=user, **link_data)
    #     return user




