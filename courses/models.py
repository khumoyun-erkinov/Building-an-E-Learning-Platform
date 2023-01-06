from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField


# Create your models here.


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    # owner  = Bu kursni kim yaratganini ko`rsatadi

    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()  # "Urlda foydalanish uchun"
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}, {self.title}'


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file'
                                     )})
    # content_type = ContentTypega ForieginKey berish uchun
    object_id = models.PositiveIntegerField()
    # primary keyga aloqador PositiveintegerField larni saqlash
    item = GenericForeignKey('content_type', 'object_id')
    # object_id and contentype aloqador fieldlarini umumiy forinkey qilish
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    # Abstract models- Django would create a table for theText model only, including the title, created, and body fields
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    # owner field kantent yaratgan foydalauchi qulaylik beradi saqlashga

    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()
    # Matn saqlash uchun


class File(ItemBase):
    file = models.FileField(upload_to='files')
    # Fayl saqlash uchun


class Image(ItemBase):
    file = models.FileField(upload_to='images')
    # Rasm saqlash uchun


class Video(ItemBase):
    url = models.URLField()
    # video saqlaydi va URL bn o`natiladi django esa yordam beradi
