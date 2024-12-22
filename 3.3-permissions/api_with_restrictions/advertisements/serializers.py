from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)
    
    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении. Проверяет, что
        у пользователя не больше 10 открытых объявлений.
        """

        user = self.context["request"].user
        limit = Advertisement.objects.filter(creator=user, status=AdvertisementStatusChoices.OPEN).count()

        if limit >= 10 and self.instance is None:
            raise serializers.ValidationError('Превышено максимальное количество открытых объявлений (10)')

        return data
