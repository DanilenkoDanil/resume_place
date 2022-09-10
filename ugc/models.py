from django.db import models
from django.conf import settings
import secrets


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name="ID пользователя в TG",
        unique=True
    )
    name = models.TextField(
        verbose_name='Имя пользователя'
    )
    status = models.BooleanField(
        verbose_name='Статус аккаунта',
        default=True
    )
    balance = models.PositiveIntegerField(
        verbose_name='Баланс',
        default=0
    )
    referral_count = models.PositiveIntegerField(
        verbose_name='Количество рефералов',
        default=0
    )
    referral_balance = models.PositiveIntegerField(
        verbose_name='Баланс от рефералов',
        default=0
    )
    ref = models.TextField(
        verbose_name='Реферальная ссылка',
        default=f'{settings.BOT_LINK}?start={secrets.token_hex(7)}'
    )
    referral = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Реферал',
        on_delete=models.PROTECT,
        null=True,
        default=None
    )

    def __str__(self):
        return f'#{self.external_id}-{self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class UsersMessage(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )

    text = models.TextField(
        verbose_name='Текст'
    )
    created_at = models.DateTimeField(
        verbose_name='Время получения',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Сообщение {self.pk} от {self.profile}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = 'Сообщения'


class BotButton(models.Model):
    number = models.PositiveIntegerField(
        verbose_name='Номер кнопки',
        unique=True
    )

    text = models.TextField(
        verbose_name='Текст'
    )

    status = models.BooleanField(
        verbose_name='Статус'
    )

    def __str__(self):
        return f'Кнопка номер - {self.number} - {self.text}'

    class Meta:
        verbose_name = "Кнопка"
        verbose_name_plural = 'Кнопки'


class BotMessage(models.Model):
    button = models.ForeignKey(
        to='ugc.BotButton',
        verbose_name='Кнопка',
        on_delete=models.PROTECT,
    )

    text = models.TextField(
        verbose_name='Текст'
    )

    def __str__(self):
        return f'Сообщение бота для кнопки - {self.button}'

    class Meta:
        verbose_name = "Сообщение Бота"
        verbose_name_plural = 'Сообщения Бота'


class Orders(models.Model):
    platform = models.TextField(
        verbose_name="Платформа",
    )
    type = models.TextField(
        verbose_name='Тип заказа'
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество'
    )
    status = models.TextField(
        verbose_name='Статус'
    )
    service = models.TextField(
        verbose_name='Сервис',
    )
    user = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Заказчик',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = 'Заказы'


class Service(models.Model):
    platform = models.TextField(
        verbose_name="Платформа",
    )
    type = models.TextField(
        verbose_name='Тип заказа'
    )
    product_id = models.TextField(
        verbose_name='ID услуги',
    )
    service = models.TextField(
        verbose_name='Сервис',
    )
    price = models.FloatField(
        verbose_name='Цена за еденицу'
    )
    min_count = models.PositiveIntegerField(
        verbose_name='Минимальное количество'
    )
    max_count = models.PositiveIntegerField(
        verbose_name='Максимальное количество'
    )
    link_form = models.TextField(
        verbose_name='Формат ссылки'
    )

    class Meta:
        verbose_name = "Сервис"
        verbose_name_plural = 'Сервис'


