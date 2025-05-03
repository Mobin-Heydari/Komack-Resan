from rest_framework import serializers
from .models import User, IdCardInFormation




class IdCardInFormationSerializer(serializers.ModelSerializer):

    class Meta:
        model = IdCardInFormation
        fields = "__all__"

    def update(self, instance, validated_data):
        request = self.context.get('request')

        if request.user.is_staff:
            instance.id_card_status == validated_data.get('id_card_status', instance.id_card_status)

        instance.id_card == validated_data.get('id_card', instance.id_card)
        instance.id_card_number == validated_data.get('id_card_number', instance.id_card_number)

        instance.save()
        return instance



# تعریف سریالایزر برای مدل کاربر
class UserSerializer(serializers.ModelSerializer):

    id_card_info = IdCardInFormationSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'id_card_info',
            'username',
            'full_name',
            'email',
            'phone',
            'user_type',
            'status',
            'joined_date',
            'last_updated',
        ]
        read_only_fields = ['id', 'joined_date', 'last_updated', 'id_card_info']