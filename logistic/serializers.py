from rest_framework import serializers

from logistic.models import *


class ProductSerializer(serializers.ModelSerializer):
    """Продукт"""
    class Meta:
        model = Product
        fields = '__all__'



class ProductPositionSerializer(serializers.ModelSerializer):
    """Позиция продукта на складе"""
    class Meta:
        model = StockProduct
        fields = ["product", "quantity", "price"]



class StockSerializer(serializers.ModelSerializer):
    """Склад"""
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = [ "address", "positions"]


    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)
        return stock

    def update_or_create(self, instance, validated_data):
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for position in positions:
            StockProduct.objects.update_or_create(stock=stock, **position)
        return stock

