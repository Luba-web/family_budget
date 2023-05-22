from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from budget.models import Category, CategoryIncome, Income, MoneyBox, Spend

User = get_user_model()


class UserSerializer(UserCreateSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = User

        fields = (
            "username",
            "email",
            "id",
            "password",
            "first_name",
            "last_name",
            "avatar",
        )


class CategoryIncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryIncome
        fields = ("id", "title", "description", "icon", "color")


class IncomeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    category = CategoryIncomeSerializer()

    class Meta:
        model = Income
        fields = ("id", "title", "user", "amount", "created", "category")


class IncomeAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = ("id", "title", "amount", "created", "category")

    def to_representation(self, instance):
        return IncomeSerializer(self).to_representation(instance)


class MoneyBoxSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = MoneyBox
        fields = (
            "id",
            "title",
            "total",
            "accumulation",
            "is_collected",
            "achieved",
            "category",
            "description",
        )
        read_only_fields = ("achieved",)

    def update(self, instance, validated_data):
        accumulation = validated_data.pop("accumulation", None)
        if accumulation is not None:
            summa = instance.accumulation + accumulation
            if instance.total < summa:
                ostotok = instance.total - instance.accumulation
                raise ValidationError(f"Для достижения цели нужно всего {ostotok}")
            instance.accumulation = summa
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        category_id = data.get("category")
        if category_id is not None:
            category = Category.objects.get(pk=category_id)
            category_serializer = CategorySerializer(category)
            data["category"] = category_serializer.data
            return data
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "id",
            "title",
            "description",
            "icon",
            "color"
        )


class SpendSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Spend
        fields = (
            "id",
            "title",
            "amount",
            "created",
            "description",
            "category",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        category_id = data.get("category")
        if category_id is not None:
            category = Category.objects.get(pk=category_id)
            category_serializer = CategorySerializer(category)
            data["category"] = category_serializer.data
            return data
        return data
