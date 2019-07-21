from rest_framework import serializers
# from whosaler_inventory.models import WSProduct, WSProductVariation
# from whosaler_inventory import constants


class MarketPlacePictureForm(serializers.Serializer):
    picture = serializers.ImageField(required=False, allow_null=True)