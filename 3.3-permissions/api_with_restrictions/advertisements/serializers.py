from django.contrib.auth.models import User
from django.forms import ValidationError
from rest_framework import serializers

from advertisements.models import Advertisement, UserFavoriteAdvertisement


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

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)
    


    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
  

        if self.context["request"].method == 'POST':
            open_adv_count = Advertisement.objects.filter(
                creator=self.context["request"].user,
                status='OPEN'
            ).count()
            if open_adv_count >= 10:
                raise ValidationError({
                    'limit_error': "Превышен лимит по открытым объявлениям (не более 10)"
                })

            if Advertisement.objects.filter(
                title=data['title'],
                creator=self.context["request"].user,
                status='OPEN'
            ):
                raise ValidationError({
                    'same_error': "У вас уже есть открытое объявление с таким наименованием"
                })
        return data
    
class UserFavoriteAdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для избранных объявлений пользователя."""
    user = UserSerializer(
        read_only=True,
    )
    
    class Meta:
        model = UserFavoriteAdvertisement
        fields = ('id', 'user', 'advertisement', 'created_at')
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    
    def validate(self, data):
        """Метод для валидации. Вызывается при добавлении объявления в избранное."""
        if self.context["request"].method == 'POST':
            if Advertisement.objects.filter(
                id=data['advertisement'].id,
                creator = self.context["request"].user
            ):
                raise ValidationError({
                    'own_error': "Нельзя добавить в избранное свои объявления"
                })

            if UserFavoriteAdvertisement.objects.filter(
                advertisement=data['advertisement'],
                user=self.context["request"].user,
            ):
                raise ValidationError({
                    'same_error': "Объявление уже добавлено в избранное"
                })
        return data
