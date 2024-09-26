from rest_framework import serializers

from .models import Clothes


class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = ("id", "name", "price", "description")

    def validate_description(self, value):
        if not isinstance(self.initial_data.get("description"), str):
            raise serializers.ValidationError("Description must be a string.")
        return value
