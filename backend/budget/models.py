from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()

COMMON_VALIDATOR = [MinValueValidator(1), MaxValueValidator(1_000_000)]

MONEYBOX_VALIDATOR = [MinValueValidator(1), MaxValueValidator(10_000_000)]


def validate_date(value):
    if value > timezone.now():
        raise ValidationError("Дата не может быть больше текущей")
    return value


class Category(models.Model):
    """Модель категорий для трат."""

    title = models.CharField("Название категории", max_length=50, unique=True)
    description = models.TextField(
        "Описание категории трат", max_length=500, blank=True, null=True
    )
    color = ColorField('HEX-код цвета', max_length=7)
    icon = models.ImageField(       
        upload_to="iconscategory",
        verbose_name="Иконка категории",
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Категории созданные пользователем",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'user'],
                name='unique_title_user_category'
            )
        ]

    def __str__(self):
        return self.title


class Balance(models.Model):
    """Модель актуального состояния средств."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="balances",
        verbose_name="Баланс пользователя",
    )
    balance = models.IntegerField("Баланс", default=0)

    class Meta:
        verbose_name = "Баланс"
        verbose_name_plural = "Балансы"

    def __str__(self):
        return f"Баланс пользователя {self.user}"


class Currency(models.Model):
    """Модель валют."""

    title = models.CharField("Полное название валюты", unique=True, max_length=50)
    code = models.CharField("Буквенный код валюты", unique=True, max_length=3)

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"
        default_related_name = "currencies"

    def __str__(self):
        return self.title


class Spend(models.Model):
    """Модель расходов и трат."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Траты пользователя"
    )
    title = models.CharField("Наименование расхода", max_length=70)
    created = models.DateTimeField("Время создания записи", validators=[validate_date])
    amount = models.PositiveIntegerField(
        "Израсходованная сумма", validators=COMMON_VALIDATOR
    )
    description = models.TextField(
        "Комментарий к расходу", max_length=500, blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория расхода",
        blank=True,
        null=True,
    )

    class Meta:
        default_related_name = "spends"
        verbose_name = "Расход средств"
        verbose_name_plural = "Расходы средств"

    def __str__(self):
        return self.title


class CategoryIncome(models.Model):
    """Модель Категорий для доходных средств."""

    title = models.CharField("Название категории", max_length=150)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="category_incomes",
        verbose_name="Категория дохода пользователя",
    )
    color = ColorField('HEX-код цвета', max_length=7)
    icon = models.ImageField(       
        upload_to="iconscategory",
        verbose_name="Иконка категории",
        blank=True,
    )
    description = models.TextField(
        "Комментарий к категории дохода", max_length=500, blank=True
    )

    class Meta:
        verbose_name = "Категория дохода"
        verbose_name_plural = "Категориb дохода"
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'user'],
                name='unique_title_user'
            )
        ]


class Income(models.Model):
    """Модель прихода средств."""

    title = models.CharField("Наименование прихода", max_length=50)
    description = models.TextField(
        "Комментарий к приходу", max_length=500, blank=True
    )
    amount = models.PositiveIntegerField(
        "Оприходованная сумму", validators=COMMON_VALIDATOR
    )
    created = models.DateTimeField("Время создания записи", auto_now_add=True, validators=[validate_date])
    category = models.ForeignKey(
        CategoryIncome,
        on_delete=models.SET_NULL,
        verbose_name="Категория дохода",
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Приходы пользователя",
    )

    class Meta:
        verbose_name = "Приход средств"
        verbose_name_plural = "Приходы средств"
        default_related_name = "incomes"

    def __str__(self):
        return self.title


class MoneyBox(models.Model):
    """Модель копилка."""

    title = models.CharField("Цель накопления", max_length=254)
    total = models.PositiveIntegerField(
        "Сумма, которую необходимо накопить", validators=MONEYBOX_VALIDATOR
    )
    accumulation = models.PositiveIntegerField(
        "Уже накоплено", validators=MONEYBOX_VALIDATOR
    )
    achieved = models.BooleanField("Цель достигнута/не достигнута", default=False)
    description = models.TextField(
        "Комментарий к приходу", max_length=500, blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория расхода",
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="moneyboxes",
        verbose_name="Цель пользователя",
    )

    class Meta:
        verbose_name = "Цель накопления"
        verbose_name_plural = "Цели накопления"
        default_related_name = "moneyboxes"

    def __str__(self):
        return self.title

    @property
    def is_collected(self):
        return self.total == self.accumulation
