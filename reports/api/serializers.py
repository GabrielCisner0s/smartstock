from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):

    total_products = serializers.IntegerField()

    active_products = serializers.IntegerField()

    low_stock_products = serializers.IntegerField()

    entries_today = serializers.IntegerField()

    exits_today = serializers.IntegerField()
    
