from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from INKLined_app.models import Customer, Artist, Review, Picture
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User



class CustomerForm(forms.ModelForm):
    USERNAME = forms.CharField(max_length=Customer.USERNAME_MAX,
                           help_text="Please enter a username.")
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    PROFILE_PICTURE = forms.ImageField(help_text = "Please enter a profile picture",initial='default_logo.jpg')

    class Meta:
        model = Customer
        fields = ('USERNAME','PROFILE_PICTURE')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.set_password(self.cleaned_data["password1"])
        if commit:
            customer.save()
        return customer

class CustomerChangeForm(forms.ModelForm):
    PASSWORD = ReadOnlyPasswordHashField(help_text = "Please enter a password")
    PROFILE_PICTURE = forms.ImageField(help_text = "Please enter a profile picture",initial='default_logo.jpg')

    class Meta:
        model = Customer
        fields = ('USERNAME', 'PASSWORD', 'PROFILE_PICTURE')

    def clean_password(self):
        return self.initial["PASSWORD"]

    

class ArtistForm(forms.ModelForm):
    ARTIST_USERNAME = forms.CharField(max_length=Artist.USERNAME_MAX,
                            help_text="Please enter a username.")

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    ADDRESS = forms.CharField(max_length=100)
    RATING = forms.IntegerField(widget=forms.HiddenInput())
    TOTAL_REVIEWS = forms.IntegerField(widget=forms.HiddenInput(),initial = 0)
    
    PROFILE_PICTURE = forms.ImageField(help_text = "Please enter a profile picture",initial='default_logo.jpg')
    FULL_NAME = forms.CharField(max_length=40,help_text = "Please enter your full name")
    CONTACT_DETAILS = forms.CharField(max_length=80, help_text="Please enter contact details.")
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
    STYLE_1 = forms.CharField(max_length = 20)
    STYLE_2 = forms.CharField(max_length = 20)
    STYLE_3 = forms.CharField(max_length = 20)


    class Meta:
        model = Artist
        fields = ('ARTIST_USERNAME','PASSWORD','ADDRESS','PROFILE_PICTURE','FULL_NAME','CONTACT_DETAILS','STYLE_1','STYLE_2','STYLE_3')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        artist = super().save(commit=False)
        artist.set_password(self.cleaned_data["password1"])
        if commit:
            artist.save()
        return artist

class ArtistChangeForm(forms.ModelForm):
    PASSWORD = ReadOnlyPasswordHashField(help_text = "Please enter a password")
    PROFILE_PICTURE = forms.ImageField(help_text = "Please enter a profile picture",initial='default_logo.jpg')
    FULL_NAME = forms.CharField(max_length=40,help_text = "Please enter your full name")
    CONTACT_DETAILS = forms.CharField(max_length=80, help_text="Please enter contact details.")
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
    STYLE_1 = forms.CharField(max_length = 20)
    STYLE_2 = forms.CharField(max_length = 20)
    STYLE_3 = forms.CharField(max_length = 20)

    class Meta:
        model = Artist
        fields = ('ARTIST_USERNAME', 'PASSWORD', 'PROFILE_PICTURE','RATING','TOTAL_REVIEWS','FULL_NAME','CONTACT_DETAILS','STYLE_1','STYLE_2','STYLE_3')

    def clean_password(self):
        return self.initial["PASSWORD"]


class ReviewForm(forms.ModelForm):
    
    PICTURE = forms.ImageField(help_text = "Please enter a tattoo picture")
 
    TITLE = forms.CharField(help_text = "Please enter a picture title",max_length=Review.TITLE_MAX_LENGTH)
    DESCRIPTION = forms.URLField(help_text = "Please enter a tattoo description",max_length = Review.DESCRIPTION_MAX_LENGTH)
    RATING = forms.IntegerField(help_text = "Please enter a tattoo rating")
    DATE = forms.DateField(help_text = "Please enter the tattoo date")


    class Meta:
        model = Review
        fields = ('ID','PICTURE','TITLE','DESCRIPTION','RATING','DATE')
        
class PictureForm(forms.ModelForm):
    UPLOADED_IMAGE = forms.ImageField(help_text = "Please enter a tattoo picture")

    class Meta:
        model=Picture
        fields = ('ID','ARTIST','UPLOADED_IMAGE')



class UserForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'password',)


