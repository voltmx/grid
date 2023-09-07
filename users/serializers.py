from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()

class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(style={"input_type": "password"})
    email = serializers.CharField()

    def validate(self, attrs):
        password = attrs.get("password")
        params = {"email": attrs.get("email")}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                raise serializers.ValidationError("invalid_credentials")
        if self.user and self.user.is_active:
            return attrs
        raise serializers.ValidationError("invalid_credentials")

