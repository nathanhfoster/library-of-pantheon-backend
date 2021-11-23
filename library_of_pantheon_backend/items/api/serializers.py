from rest_framework.serializers import ModelSerializer, JSONField, Field
from pwa_store_backend.users.models import User
from rest_framework import serializers
from ..models import Item, Category, ItemScreenshot, ItemAnalytics
from pwa_store_backend.users.models import User


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)
        read_only_fields = ('created_at', 'updated_at')


class ItemAnalyticsSerializer(ModelSerializer):
    class Meta:
        model = ItemAnalytics
        fields = ('view_count', 'launch_count', 'rating_avg', 'rating_count', )


class ItemMinimalSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'slug', 'name', 'url', 'image_url',)
        read_only_fields = ('id', 'created_at', 'updated_at', 'categories')


class ItemSerializer(ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Item
        fields = ('id', 'slug', 'published', 'name', 'url', 'description',
                  'categories', 'image_url', 'updated_at',)
        lookup_field = 'slug'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)
        categories = self.context['request'].data.get('categories', None)
        if categories:
            obj.categories.set(list(Category.objects.filter(name__in=categories)))
            obj.save()
        return obj

    def create(self, validated_data):
        obj = super().create(validated_data)
        categories = self.context['request'].data.get('categories', None)
        if categories:
            obj.categories.set(list(Category.objects.filter(name__in=categories)))
            obj.save()
        return obj


class ItemDetailSerializer(ItemSerializer):

    class Meta(ItemSerializer.Meta):
        fields = ItemSerializer.Meta.fields + ('created_by', 'updated_by', )
