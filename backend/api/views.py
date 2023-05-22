from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsAuthor
from .serializers import (CategoryIncomeSerializer, CategorySerializer,
                          IncomeAddSerializer, IncomeSerializer,
                          MoneyBoxSerializer, SpendSerializer)
from budget.models import Category, CategoryIncome, Income, MoneyBox, Spend


class MoneyBoxViewSet(viewsets.ModelViewSet):

    serializer_class = MoneyBoxSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        return MoneyBox.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(detail=True, methods=("post",))
    def goal_achieved(self, request, pk=None):
        moneybox = MoneyBox.objects.get(id=pk)
        if moneybox.achieved:
            return Response({"Так-так": "Цель уже достигнута"})
        if moneybox.is_collected:
            moneybox.achieved = True
            moneybox.save()
            Spend.objects.create(
                title=moneybox.title,
                amount=moneybox.total,
                description=moneybox.description,
                category=moneybox.category,
                user=request.user,
                created=timezone.now()
            )
            return Response({"Браво": "Цель достигнута"})
        return Response({"Так-так": "Работай больше, иди копи еще"})


class IncomeViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthor,)

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return IncomeAddSerializer
        return IncomeSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CategoryIncomeViewSet(viewsets.ModelViewSet):

    serializer_class = CategoryIncomeSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        return CategoryIncome.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthor,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SpendViewSet(viewsets.ModelViewSet):

    queryset = Spend.objects.all()
    serializer_class = SpendSerializer
    permission_classes = (IsAuthor,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
