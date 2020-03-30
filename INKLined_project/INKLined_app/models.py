from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    USERNAME_MAX = 30
    PASSWORD_MAX = 10000
    USERNAME = models.CharField(max_length=USERNAME_MAX, unique=True)
    PASSWORD = models.CharField(max_length=PASSWORD_MAX)
    PROFILE_PICTURE = models.ImageField(upload_to='profile_images',blank=True)

    class Meta:
        verbose_name_plural = 'Customers'

    
    def __str__(self):
        return self.USERNAME

class Artist(models.Model):
    NATURE_STYLE = 1
    CARTOON_STYLE = 2
    ABSTRACT_STYLE = 3
    GEOMETRIC_STYLE = 4
    REALISM_STYLE = 5
    TRIBAL_STYLE = 6
    SLEAVE_STYLE = 7
    WRITING_STYLE = 8
    NON_ENGLISH_WRITING_STYLE = 9
    OTHER_STYLE = 10
    STYLE_CHOICES = (
        (NATURE_STYLE,"Nature"),
        (CARTOON_STYLE,"Cartoon"),
        (ABSTRACT_STYLE,"Abstract"),
        (GEOMETRIC_STYLE,"Geometric"),
        (REALISM_STYLE,"Realism"),
        (TRIBAL_STYLE,"Tribal"),
        (SLEAVE_STYLE,"Sleave"),
        (WRITING_STYLE,"Writing"),
        (NON_ENGLISH_WRITING_STYLE,"Non-english Writing"),
        (OTHER_STYLE,"Other"),
        )
    USERNAME_MAX = 30
    PASSWORD_MAX = 10000
    
    ARTIST_USERNAME = models.CharField(max_length=USERNAME_MAX, unique=True)
    PASSWORD = models.CharField(max_length=PASSWORD_MAX)
    ADDRESS = models.CharField(max_length=100)
    RATING = models.IntegerField(default = None)
    TOTAL_REVIEWS = models.IntegerField(default = 0)
    PROFILE_PICTURE = models.ImageField(upload_to='profile_images', blank=True)
    FULL_NAME = models.CharField(max_length=40)
    CONTACT_DETAILS = models.CharField(max_length=80)
    STYLE_1 = models.CharField(max_length = 20)
    STYLE_2 = models.CharField(max_length = 20 , blank=True)
    STYLE_3 = models.CharField(max_length = 20, blank = True)

    class Meta:
        verbose_name_plural = 'Artists'
    
    def __str__(self):
        return self.ARTIST_USERNAME
    
    
class Review(models.Model):
    RATING_CHOICES = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
        )
    TITLE_MAX_LENGTH = 50
    DESCRIPTION_MAX_LENGTH = 200
    ID = models.AutoField(auto_created = True,primary_key=True)
    PICTURE = models.ImageField(upload_to='review_images', blank=False)
    CUSTOMER = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ARTIST = models.ForeignKey(Artist, on_delete=models.CASCADE)
    TITLE = models.CharField(max_length=TITLE_MAX_LENGTH)
    DESCRIPTION = models.URLField(max_length = DESCRIPTION_MAX_LENGTH)
    RATING = models.IntegerField(choices = RATING_CHOICES,null=True)
    DATE = models.DateField(null=True)
    
    def __str__(self):
        return str(self.ID)

class Picture(models.Model):
    ID = models.AutoField(auto_created = True,primary_key=True)
    ARTIST = models.ForeignKey(Artist, on_delete=models.CASCADE)
    UPLOADED_IMAGE = models.ImageField(upload_to='artist_images', blank=False)

    class Meta:
        verbose_name_plural = 'Pictures'

    def __str__(self):
        return str(self.ID)

class Saves(models.Model):
    CUSTOMER = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ARTIST = models.ForeignKey(Artist, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Saves'

    def __str__(self):
        return str(self.CUSTOMER.USERNAME + ' has saved ' +self.ARTIST.ARTIST_USERNAME)


