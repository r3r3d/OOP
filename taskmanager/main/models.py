from audioop import reverse

from django.dispatch import Signal
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.db import models
from .utilities import get_timestamp_path
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class AdvUser(AbstractUser):
    middle_name = models.CharField('Отчество', max_length=50)
    last_name = models.CharField(max_length=12, verbose_name="Фамилия", validators=[
        RegexValidator(regex=r'[а-яА-ЯёЁ]+$', message='Фамилия введена не правильно',
                       code='invalid_last_name'), ])
    first_name = models.CharField(max_length=12, verbose_name="Имя", validators=[
        RegexValidator(regex=r'[а-яА-ЯёЁ]+$', message='Имя введено не правильно',
                       code='invalid_first_name'), ])
    middle_name = models.CharField(max_length=12, verbose_name="Отчество", validators=[
        RegexValidator(regex=r'[а-яА-ЯёЁ]+$', message='Отвество введено не правильно',
                       code='invalid_middle_name'), ])
    role = models.CharField(max_length=254, verbose_name='Роль',
                            choices=(('admin', 'Администратор'), ('user', 'Пользователь'), ('author', 'Автор')), default='user')
    username = models.CharField(max_length=20, verbose_name="Имя пользователя", unique=True, validators=[
        RegexValidator(regex=r'^[a-z]+$', message='Имя пользователя введено не правильно',
                       code='invalid_username'), ])

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    def is_author(self, bb):
        if self.pk == bb.author.pk:
            return True
        return False

    class Meta(AbstractUser.Meta):
        pass


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True,
                            verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True,
                                     verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric',
                                     on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name='Надрубрика')


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    object = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    object = SubRubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'


class Bb(models.Model):
    STATUS_CHOISES = [
        ('new', 'новый'),
        ('confirmed', 'Принято в работу'),
        ('canceled', 'Выполнено')
    ]
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=40, verbose_name='Товар')
    content = models.TextField(verbose_name='Описание')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Автор объявления')
    imageses = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name=' Доп Изображение')
    commented = models.TextField(default='', verbose_name='Комментарий')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    status = models.CharField(max_length=254, verbose_name='Статус',
                              choices=STATUS_CHOISES,
                              default='new')
    counter = models.IntegerField(null=True, blank=True, verbose_name='счетчик')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('rubric/detail.html', args=[str(self.id)])

    def get_status_name(self):
        for status in self.STATUS_CHOISES:
            if status[0] == self.status:
                return status[1]
        return 'Не задан'

    def str(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Объявл'
        verbose_name = 'Объявление'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'
