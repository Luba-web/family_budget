from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, _lazy_re_compile
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _
from django.utils.translation import ngettext

PASSWORD_CHARS_RE = _lazy_re_compile(r"^[a-zA-Z\d!\"#$%&., ]+\Z")


simple_name_re = _lazy_re_compile(r"^([^\W\d_]|[\s-])+$")
validate_simple_name = RegexValidator(
    simple_name_re,
    _(
        "Enter a valid `name` value consisting of only letters "
        "and symbols `-`."
    ),
    "invalid",
)


@deconstructible
class UnicodeUsernameValidator(RegexValidator):
    regex = r"^[a-zA-Z\d_.+-]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters(a-z), "
        "numbers, and ./+/-/_ characters."
    )
    flags = 0


class PasswordCharValidator:
    """Валидатор допустимого набора символов для пароля."""

    def validate(self, password, user=None):
        if not PASSWORD_CHARS_RE.search(str(password)):
            raise ValidationError(
                _(
                    "The password must contain chars a-z or digits or "
                    'special character: `!"#$%&., `'
                ),
                code="password_no_symbol",
            )

    def get_help_text(self):
        return _(
            "The password must contain chars a-z or digits or "
            'special character: `!"#$%&., `'
        )


class MaximumLengthValidator:
    """Валидация пароля на максимальную длину."""

    def __init__(self, max_length=40):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                ngettext(
                    "This password is too long. It must contain no more than "
                    "%(max_length)d character.",
                    "This password is too long. It must contain no more than "
                    "%(max_length)d characters.",
                    self.max_length,
                ),
                code="password_too_long",
                params={"max_length": self.max_length},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain "
            "no more than %(max_length)d characters.",
            "Your password must contain "
            "no more than %(max_length)d characters.",
            self.max_length,
        ) % {"max_length": self.max_length}