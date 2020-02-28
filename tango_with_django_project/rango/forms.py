from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from rango.models import Customer, Artist, Review
from django.contrib.auth.models import User


class CustomerForm(forms.ModelForm):
    USERNAME = forms.CharField(max_length=Customer.USERNAME_MAX,
                           help_text="Please enter a username.")
    PASSWORD = forms.IntegerField(widget=forms.PasswordInput, help_text="Please enter a password." )
    PROFILE_PICTURE = forms.ImageField(help_text = "Please enter a profile picture",initial='default_logo.jpg')

    class Meta:
        model = Customer
        fields = ('USERNAME','PASSWORD','PROFILE_PICTURE')

class ArtistForm(forms.ModelForm):
    ARTIST_USERNAME = forms.CharField(max_length=Artist.USERNAME_MAX,
                            help_text="Please enter a username.")
    PASSWORD = forms.IntegerField(widget=forms.PasswordInput, help_text="Please enter a password." )
    
    ADDRESS = forms.CharField(max_length=100)
    RATING = forms.IntegerField(widget=forms.HiddenInput())
    TOTAL_REVIEWS = forms.IntegerField(widget=forms.HiddenInput(),initial = 0)
    
    PROFILE_PICTURE = forms.ImageField(help_text = "Please enter a profile picture",initial='default_logo.jpg')
    FULL_NAME = forms.CharField(max_length=40,help_text = "Please enter your full name")
    CONTACT_DETAILS = forms.CharField(max_length=80, help_text="Please enter contact details.")
    STYLE = forms.CharField(max_length = 20)


    class Meta:
        model = Artist
        fields = ('ARTIST_USERNAME','PASSWORD','ADDRESS','PROFILE_PICTURE','FULL_NAME','CONTACT_DETAILS','STYLE')


class ReviewForm(forms.ModelForm):
    
    PICTURE = forms.ImageField(help_text = "Please enter a tattoo picture")
 
    TITLE = forms.CharField(help_text = "Please enter a picture title",max_length=Review.TITLE_MAX_LENGTH)
    DESCRIPTION = forms.URLField(help_text = "Please enter a tattoo description",max_length = Review.DESCRIPTION_MAX_LENGTH)
    RATING = forms.IntegerField(help_text = "Please enter a tattoo rating")
    DATE = forms.DateField(help_text = "Please enter the tattoo date")


    class Meta:
        model = Review
        fields = ('ID','PICTURE','TITLE','DESCRIPTION','RATING','DATE')

def add_review(request, USERNAME, ARTIST_USERNAME):
    try:
        customer = Customer.objects.get(USERNAME=USERNAME)
    except Customer.DoesNotExist:
        customer = None

    try:
        artist = Artist.objects.get(ARTIST_USERNAME=ARTIST_USERNAME)
    except Artist.DoesNotExist:
        artist = None
        
    # You cannot add a review to a artist or customer that does not exist...
    if customer is None or artist is None:
        return redirect('/rango/')
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
    if form.is_valid():
        if customer and artist:
            review = form.save(commit=False)
            review.CUSTOMER = customer
            review.ARTIST = artist
            review.save()
            return redirect(reverse('rango:show_artist',
                                    kwargs={'ARTIST_USERNAME':
                                            ARTIST_USERNAME}))
    else:
        print(form.errors)

    context_dict = {'form': form, 'Customer': customer}
    return render(request, 'rango/add_review.html', context=context_dict)


    class Meta:
        model = Review
        fields = ('ID','PICTURE','CUSTOMER','ARTIST','TITLE','DESCRIPTION','RATING','DATE')


