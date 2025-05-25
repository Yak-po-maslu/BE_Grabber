from rest_framework import serializers
import re


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate_new_password(self, value):
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

        # 5. Хотя бы один спецсимвол
        special_symbols_pattern = r'[!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?]'
        if not re.search(special_symbols_pattern, value):
                errors.append(f"Password must contain at least one special character:{special_symbols_pattern}")

        allowed = r'^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?]+$'

        # 6. Только латинские символы и спецсимволы
        if not re.fullmatch(allowed, value):
            errors.append(
                "Password may contain only Latin letters, digits and the following special characters: !@#$%^&*()_+-=[]{};':\"\\|,.<>/?"
            )

        if errors:
            raise serializers.ValidationError(errors)

        return value