from typing import cast

from rest_framework import serializers
import re



from users.views import CustomUser


class ChangePasswordValidator(serializers.Serializer):
    old_password = serializers.CharField(write_only=True,required=True)
    new_password = serializers.CharField(write_only=True,required=True)

    def validate_old_password(self, value):
        user = cast(CustomUser, self.context['request'].user)
        if not user.check_password(value):
            raise serializers.ValidationError('Invalid old password')
        return value


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

        # 5. Только латинские символы
        if not re.fullmatch(r'[A-Za-z0-9]+', value):
            errors.append("Password must contain only Latin letters and digits.")

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def save(self):
        user = self.context['request'].user
        try:
            user.set_password(self.validated_data['new_password'])
            user.save()
        except Exception as e:
            raise serializers.ValidationError(str(e))
