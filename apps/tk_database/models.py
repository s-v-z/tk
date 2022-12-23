from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# enums
class Employment(models.TextChoices):
    UNEMPLOYED = 'unemployed', 'Безработный(-ая)'
    EMPLOYED = 'employed', 'Трудоустроен(-а)'
    STUDENT = 'student', 'Студент(-ка)'
    UNKNOWN = 'unknown', 'Неизвестно'

class SportsCategory(models.TextChoices):
    THIRD = '3', 'Третья'
    SECOND = '2', 'Вторая'
    FIRST = '1', 'Первая'
    CANDIDATE = 'KMS', 'КМС'
    MASTER = 'MASTER', 'Мастер спорта'

class InstructorCategory(models.TextChoices):
    INSTRUCTOR = 'instructor', 'Инструктор'
    SENIOR_INSTRUCTOR = 'senior_instructor', 'Старший инструктор'

class HikeCategory(models.IntegerChoices):
    CAT_0 = 0, 'н/к'
    CAT_1 = 1, 'Первая' 
    CAT_2 = 2, 'Вторая'
    CAT_3 = 3, 'Третья'
    CAT_4 = 4, 'Четвертая'
    CAT_5 = 5, 'Пятая'
    CAT_6 = 6, 'Шестая'

class HikeSubCategory(models.IntegerChoices):
    SUB_1 = 1, 'с эл. 1' 
    SUB_2 = 2, 'с эл. 2'
    SUB_3 = 3, 'с эл. 3'
    SUB_4 = 4, 'с эл. 4'
    SUB_5 = 5, 'с эл. 5'
    SUB_6 = 6, 'с эл. 6'

# db models
class GeoRegion(models.Model):
    name            = models.CharField(max_length=255)
    def __str__(self):
         return self.name


class HikeType(models.Model):
    name            = models.CharField(max_length=255)
    short_name      = models.CharField(max_length=100)
    def __str__(self):
         return self.name


class UserProfile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    sex             = models.CharField(max_length=1, choices=[('M', 'Муж.'), ('F', 'Жен.'), ('U', 'Неизвестен')], default='U')
    birthday        = models.DateField(default=None, blank=True, null=True)
    phone_home      = models.CharField(max_length=32, default=None, blank=True, null=True)
    phone_mobile    = models.CharField(max_length=32, default=None, blank=True, null=True)
    phone_relative  = models.CharField(max_length=32, default=None, blank=True, null=True)
    employment      = models.CharField(max_length=32, choices=Employment.choices, default=Employment.UNKNOWN)
    work_place      = models.CharField(max_length=1024, default=None, blank=True, null=True)
    sports_category = models.CharField(max_length=32, choices=SportsCategory.choices, default=None, blank=True, null=True)
    sports_category_expiration_date = models.DateField(default=None, blank=True, null=True)
    max_height      = models.IntegerField(default=0)
    max_camp_height = models.IntegerField(default=0)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Hike(models.Model):
    type            = models.ForeignKey(HikeType, on_delete=models.RESTRICT)
    category        = models.IntegerField(choices=HikeCategory.choices, default=None, blank=True, null=True)
    sub_category    = models.IntegerField(choices=HikeSubCategory.choices, default=None, blank=True, null=True)
    region          = models.ForeignKey(GeoRegion, on_delete=models.RESTRICT, default=None, blank=True, null=True)
    title           = models.CharField(max_length=255)
    description     = models.TextField()
    image           = models.ImageField(upload_to='hike_pics', default=None, blank=True, null=True)
    leader          = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='hike_leader')
    instructor      = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='hike_instructor', default=None, blank=True, null=True)
    start_date      = models.DateField()
    end_date        = models.DateField()
    is_completed    = models.BooleanField()
    is_private      = models.BooleanField()
    is_full         = models.BooleanField()
    def __str__(self):
         return self.type.name + ' ' + str(self.category) + ' ' + self.region.name + ' ' + self.title


class HikeMember(models.Model):
    hike            = models.ForeignKey(Hike, on_delete=models.CASCADE)
    user            = models.ForeignKey(User, on_delete=models.RESTRICT)
    role_name       = models.CharField(max_length=255)


class HikeReport(models.Model):
    hike              = models.ForeignKey(Hike, null=False, on_delete=models.CASCADE)
    actual_start_date = models.DateField()
    actual_end_date   = models.DateField()
    actual_path       = models.TextField()
    report_file       = models.FilePathField(path="/report")
    report_url        = models.URLField()