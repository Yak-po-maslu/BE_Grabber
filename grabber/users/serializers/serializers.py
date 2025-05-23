from rest_framework import serializers
from ..views import CustomUser
import re

User = CustomUser

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name','phone_number', 'role', 'date_joined', 'location','user_photo']
        extra_kwargs = {
            'email': {'required': True},
        }
        read_only_fields = ['role', 'date_joined', 'id']

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


class UserLoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name','phone_number', 'role', 'date_joined', 'location']
        extra_kwargs = {
            'email': {'required': True},
        }
        read_only_fields = ['role', 'date_joined', 'id']
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
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    role = serializers.ChoiceField(
        choices=[
            (User.Roles.BUYER, "Покупець"),
            (User.Roles.SELLER, "Продавець"),
        ],
        required=False,
        default=User.Roles.SELLER
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password','role']

    def validate_email(self, value):
        value = value.strip().lower()
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("First name cannot be empty.")
        return value

    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Last name cannot be empty.")
        return value

    def validate_phone_number(self, value):

        value = value.strip()

        # Проверка формата: начинается с +, дальше только цифры
        if not re.fullmatch(r'\+380\d{9}', value):
            raise serializers.ValidationError(
                "Phone number must be in format +380XXXXXXXXX (12 digits after +380, no spaces or symbols)."
            )

        return value

    def validate_password(self, value):
        errors = []

        # 1. Минимальная длина
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long.")

        # 2. Заглавная буква
        if not re.search(r'[A-Z]', value):
            errors.append("Password must contain at least one uppercase letter.")

        # 3. Строчная буква
        if not re.search(r'[a-z]', value):
            errors.append("Password must contain at least one lowercase letter.")

        # 4. Цифра
        if not re.search(r'[0-9]', value):
            errors.append("Password must contain at least one digit.")

        # 5. Только латинские символы
        if not re.fullmatch(r'[A-Za-z0-9]+', value):
            errors.append("Password must contain only Latin letters and digits.")

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def validate_role(self, value):
        forbidden_roles = ['admin', 'moderator']
        if value in forbidden_roles:
            raise serializers.ValidationError("You cannot assign this role.")
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


