from django.db import models
from django.conf import settings


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name="ID пользователя в TG",
        unique=True
    )
    name = models.TextField(
        verbose_name='Имя пользователя'
    )
    rate = models.IntegerField(
        verbose_name='Рейтинг',
        default=0
    )
    notification = models.BooleanField(
        verbose_name='Оповещение',
        default=True
    )
    block = models.BooleanField(
        verbose_name='Блокировка',
        default=False
    )
    contacts = models.TextField(
        default=''
    )
    photo = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'#{self.external_id}-{self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class BotButton(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    text_eng = models.TextField(
        verbose_name='Text'
    )
    status = models.BooleanField(
        verbose_name='Статус'
    )

    def __str__(self):
        return f'Кнопка - {self.text}'

    class Meta:
        verbose_name = "Кнопка"
        verbose_name_plural = 'Кнопки'


class BotMessage(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    text_eng = models.TextField(
        verbose_name='Text'
    )

    def __str__(self):
        return f'Сообщение бота для кнопки - {self.id}'

    class Meta:
        verbose_name = "Сообщение Бота"
        verbose_name_plural = 'Сообщения Бота'


class WorkType(models.Model):
    type_name = models.CharField(max_length=150)
    subtype_status = models.BooleanField(default=False)
    relates_to = models.ForeignKey(to='WorkType', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.type_name}'

    class Meta:
        verbose_name = "Тип работы"
        verbose_name_plural = 'Типы работ'


class Resume(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'Резюме - {self.user.name}'

    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = 'Резюме'


class WorkTypeResume(models.Model):
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        verbose_name = "Тип работы для резюме"
        verbose_name_plural = "Типы работы для резюме"


class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
