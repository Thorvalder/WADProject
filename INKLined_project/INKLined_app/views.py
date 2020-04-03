#Importing required libraries
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from INKLined_app.models import Customer,Artist,Review,Saves,Picture
from INKLined_app.forms import CustomerForm, ArtistForm, ReviewForm, PictureForm
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User


#home page view which lists the top five artists and sends the user to the home page
def index(request):
    top_artist_list = Artist.objects.order_by('-RATING')[:5]
    context_dict = {}
    context_dict['top_artists'] = top_artist_list

    response = render(request, 'INKLined_app/home.html', context=context_dict)
    return response

#view for logging in the user
def login_user(request):

    #checks if the user is already logged in and if so then it sends them to their account page
    if request.user.is_authenticated:
        return redirect('INKLined_app:show_account')

    #if the user is submitting the log in form then the view attempts to authenticate their entered details
    if request.method == 'POST':
        try:
            usertype = 'customer'
            USERNAME = request.POST.get('username')
            PASSWORD = request.POST.get('password')
            print(PASSWORD)
            print("trying to auth customer")
            user = authenticate(username=USERNAME, password=PASSWORD)
            print("authed customer")
        except:
            print('bad login')
            
        #if the user has authenticated then it checks to see if the user is a customer or artist and sends details to the context dictionary accordingly
        if user:
            print(user.password)
            login(request, user)
            context_dict = {}
            try:
                u = Customer.objects.get(USERNAME=user.username)
                usertype='customer'
            except:
                usertype='artist'
            if usertype == 'customer':
                u = Customer.objects.get(USERNAME=USERNAME)
                context_dict['USERTYPE'] = usertype
                context_dict['USERNAME'] = u.USERNAME
                context_dict['PROFILE_PICTURE'] = u.PROFILE_PICTURE
            else:
                u = Artist.objects.get(ARTIST_USERNAME=USERNAME)
                context_dict['ARTIST_USERNAME'] = u.ARTIST_USERNAME
                context_dict['ADDRESS'] = u.ADDRESS
                context_dict['PROFILE_PICTURE'] = u.PROFILE_PICTURE
                context_dict['FULL_NAME'] = u.FULL_NAME
                context_dict['CONTACT_DETAILS'] = u.CONTACT_DETAILS
                context_dict['STYLE_1'] = u.STYLE_1
                context_dict['STYLE_2'] = u.STYLE_2
                context_dict['STYLE_3'] = u.STYLE_3
                
            #Joseph added next line for css header button:
            context_dict['pageIsLogin']=True
            response = render(request, 'INKLined_app/my-account.html', context=context_dict)
            return response
            
        else:
            print(f"Invalid login details")
            return HttpResponse("Invalid login details supplied.")
    else:
        #Joseph added next two lines for css header button:
        context_dict = {}
        context_dict['pageIsLogin']=True
        return render(request, 'INKLined_app/login.html', context=context_dict)


#view for logging users out
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('INKLined_app:index'))


#view for showing a user their account details
def show_account(request):

    #if the user is not logged in then it sends them to the login page, otherwise it will determine if they are a customer or artist
    if request.user.is_authenticated:
        USERNAME = request.user.username
    else:
        return redirect('INKLined_app:login')
        
    context_dict = {}
    try:
        customer = Customer.objects.get(USERNAME = USERNAME)
        context_dict['account'] = customer
        context_dict['USERNAME'] = USERNAME
        context_dict['USERTYPE'] = True
        context_dict['PROFILE_PICTURE'] = customer.PROFILE_PICTURE
    except:
        try:
            artist = Artist.objects.get(ARTIST_USERNAME = USERNAME)
            context_dict['account'] = artist
            context_dict['ARTIST_USERNAME'] = USERNAME
            context_dict['PROFILE_PICTURE'] = artist.PROFILE_PICTURE
            context_dict['FULL_NAME'] = artist.FULL_NAME
            context_dict['CONTACT_DETAILS'] = artist.CONTACT_DETAILS
            context_dict['ADDRESS'] = artist.ADDRESS
            context_dict['STYLE_1'] = artist.STYLE_1
            context_dict['STYLE_2'] = artist.STYLE_2
            context_dict['STYLE_3'] = artist.STYLE_3
        except:
             context_dict['account'] = None
            
    context_dict['pageIsLogin']=True
    return render(request, 'INKLined_app/my-account.html', context=context_dict)


def show_saved(request):
    USERNAME = request.user.username
    context_dict = {}
    customer = Customer.objects.get(USERNAME = USERNAME)
    saves = Saves.objects.filter(CUSTOMER=customer)

    PICTURES = []
    ARTISTS_WITHOUT_PICTURES = []
    for save in saves:
        try:
            picture = Picture.objects.filter(ARTIST = save.ARTIST)[0]
            PICTURES = PICTURES + [picture]
        except:
            ARTISTS_WITHOUT_PICTURES = ARTISTS_WITHOUT_PICTURES + [save.ARTIST]
            
    context_dict['account'] = customer
    context_dict['PICTURES']=PICTURES
    context_dict['ARTISTS_WITHOUT_PICTURES']=ARTISTS_WITHOUT_PICTURES
    print(saves)
    
    return render(request, 'INKLined_app/saved-artists.html', context=context_dict)

def sign_up(request):
    context_dict = {}
    #Joseph added next line for CSS
    context_dict['pageIsSignUp']=True;

    return render(request, 'INKLined_app/sign-up.html', context=context_dict)

def delete_account(request):
    if request.user.is_authenticated:
        USERNAME = request.user.username
        USER = request.user
    else:
        return redirect(reverse('INKLined_app:login'))

    logout(request)
    USER.delete()
    
    try:
        customer = Customer.objects.get(USERNAME = USERNAME)
        customer.delete()
    except:
        ARTIST_USERNAME = USERNAME
        artist = Artist.objects.get(ARTIST_USERNAME = ARTIST_USERNAME)
        artist.delete()

    return redirect(reverse('INKLined_app:index'))

def artists(request):
    artists = Artist.objects.filter()
    PICTURES = []
    ARTISTS_WITHOUT_PICTURES = []
    for artist in artists:
        try:
            picture = Picture.objects.filter(ARTIST = artist)[0]
            PICTURES = PICTURES + [picture]
        except:
            ARTISTS_WITHOUT_PICTURES = ARTISTS_WITHOUT_PICTURES + [artist]
            
    context_dict = {}
    context_dict['PICTURES']=PICTURES
    context_dict['ARTISTS_WITHOUT_PICTURES']=ARTISTS_WITHOUT_PICTURES
    return render(request, 'INKLined_app/artists.html', context=context_dict)
    

def show_artist(request, ARTIST_USERNAME):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        artist = Artist.objects.get(ARTIST_USERNAME = ARTIST_USERNAME)
        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        reviews = Review.objects.filter(ARTIST = artist)

        # Adds our results list to the template context under name pages.
        context_dict['reviews'] = reviews
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['artist'] = artist
        pictures=Picture.objects.filter(ARTIST=artist)
        context_dict['pictures'] = pictures
        context_dict['PROFILE_PICTURE'] = artist.PROFILE_PICTURE
        context_dict['gmaps_location'] = "https://www.google.com/maps/embed/v1/place?q="+artist.ADDRESS.replace(" ","+")+",+Glasgow,+UK&key=AIzaSyDrnqDTlBB6vGWaMmrb7zCkap09boRPslk"

        try:
            usernameC = request.user.username
            customer = Customer.objects.get(USERNAME = usernameC)
            save = Saves.objects.get(CUSTOMER=customer,ARTIST=artist)
            context_dict['AlreadySaved'] = True
        except:
            context_dict['AlreadySaved'] = False
            
    except Artist.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything
        # the template will display the "no category" message for us.
        context_dict['artist'] = None
        context_dict['reviews'] = None
        return render(request, 'INKLined_app/artists.html', context=context_dict)
    # Go render the response and return it to the client. +
    try:
        USERNAME = request.user.username
        customer = Customer.objects.get(USERNAME = USERNAME)
        context_dict['USERTYPE'] = True
    except:
        context_dict['USERTYPE'] = False
        
    return render(request, 'INKLined_app/ARTIST_USERNAME.html', context=context_dict)

def add_picture(request):

    if not request.user.is_authenticated:
        return redirect('INKLined_app:login')
    
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        picture_form = PictureForm(request.POST)
            
        # If the form is valid...
        if picture_form.is_valid():
            
            if 'UPLOADED_IMAGE' not in request.FILES:
                print("Must have picture")
                picture_form = PictureForm()
                artist = Artist.objects.get(ARTIST_USERNAME= request.user.username)
                return render(request,'INKLined_app/add_picture.html',context={'artist':artist,
                                                                      'picture_form':picture_form})
            # Save the review data to the database.
            picture = picture_form.save(commit=False)
            picture.UPLOADED_IMAGE = request.FILES['UPLOADED_IMAGE']
            picture.ARTIST = Artist.objects.get(ARTIST_USERNAME= request.user.username)
            picture.save()
            return redirect(reverse('INKLined_app:show_artist',
                                    kwargs={'ARTIST_USERNAME':
                                            request.user.username}))
		

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(review_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        picture_form = PictureForm()
        artist = Artist.objects.get(ARTIST_USERNAME= request.user.username)
        # Render the template depending on the context.
        return render(request,'INKLined_app/add_picture.html',context={'artist':artist,
                                                                      'picture_form':picture_form})


def show_reviews(request, ARTIST_USERNAME):
    artist = Artist.objects.get(ARTIST_USERNAME=ARTIST_USERNAME)
    reviews = Review.objects.filter(ARTIST=artist)
    context_dict = {'reviews':reviews}
    context_dict['artist'] = artist
    user = request.user.username
    context_dict['not_artist'] = True
    try:
        a = Artist.objects.get(ARTIST_USERNAME=user)
        context_dict['not_artist'] = False
    except:
        pass
        
    return render(request, 'INKLined_app/reviews.html', context=context_dict)

def save_artist(request, ARTIST_USERNAME):
    USERNAME = request.user.username
    customer = Customer.objects.get(USERNAME=USERNAME)
    artist = Artist.objects.get(ARTIST_USERNAME = ARTIST_USERNAME)
    try:
        save = Saves.objects.get(CUSTOMER=customer,ARTIST=artist)
        save.delete()
    except:
        save = Saves.objects.create(CUSTOMER=customer,ARTIST=artist)

    reviews = Review.objects.filter(ARTIST = artist)
    context_dict = {}

    # Adds our results list to the template context under name pages.
    context_dict['reviews'] = reviews
    # We also add the category object from
    # the database to the context dictionary.
    # We'll use this in the template to verify that the category exists.
    context_dict['artist'] = artist
    context_dict['gmaps_location'] = "https://www.google.com/maps/embed/v1/place?q="+artist.ADDRESS.replace(" ","+")+",+Glasgow,+UK&key=AIzaSyDrnqDTlBB6vGWaMmrb7zCkap09boRPslk"
    return redirect(reverse('INKLined_app:show_artist' , args=[artist]))

    
def add_review(request, ARTIST_USERNAME):

    if not request.user.is_authenticated:
        return redirect('INKLined_app:login')
    
    # A boolean value for telling the template
    # whether the review adding was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    reviewed = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        print("posting")
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        review_form = ReviewForm(request.POST)
            
        # If the form is valid...
        if review_form.is_valid():
            #checks to see if the picture has been added, if not then sends back to add review page with fresh form
            if 'PICTURE' not in request.FILES:
                print("Must have picture")
                review_form = ReviewForm()
                artist = Artist.objects.get(ARTIST_USERNAME= ARTIST_USERNAME)
                return render(request,'INKLined_app/add_review.html',context={'artist':artist,
                                                                      'review_form':review_form})
            # Save the review data to the database.
            review = review_form.save(commit=False)
            review.PICTURE = request.FILES['PICTURE']
            review.CUSTOMER = Customer.objects.get(USERNAME = request.user.username)
            artist = Artist.objects.get(ARTIST_USERNAME= ARTIST_USERNAME)
            review.ARTIST = artist
            if type(artist.RATING) == type(int):
                artist.RATING = int(((artist.RATING*artist.TOTAL_REVIEWS) + review.RATING)/(artist.TOTAL_REVIEWS+1))
                artist.TOTAL_REVIEWS += 1
            else:
                artist.RATING = review.RATING
                artist.TOTAL_REVIEWS = 1
            review.save()
            artist.save()
            return redirect(reverse('INKLined_app:show_artist',
                                    kwargs={'ARTIST_USERNAME':
                                            ARTIST_USERNAME}))
		

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(review_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        review_form = ReviewForm()
        artist = Artist.objects.get(ARTIST_USERNAME= ARTIST_USERNAME)
        # Render the template depending on the context.
        return render(request,'INKLined_app/add_review.html',context={'artist':artist,
                                                                      'review_form':review_form})
        



def register_customer(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        customer_form = CustomerForm(request.POST)
        #profile_form = UserProfileForm(request.POST)
        # If the two forms are valid...
        if customer_form.is_valid():
            # Save the user's form data to the database.
            customer = customer_form.save()
            # Now we hash the PASSWORD with the set_PASSWORD method.
            # Once hashed, we can update the user object.
            user = User.objects.get_or_create(username=customer.USERNAME,password=customer.PASSWORD)[0]
            user.set_password(customer.PASSWORD)
            user.save()
            
            if 'PROFILE_PICTURE' in request.FILES:
                customer.PROFILE_PICTURE =  request.FILES['PROFILE_PICTURE']
            else:
                customer.PROFILE_PICTURE =  'profile_images/user.png'
                
            customer.save()

            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(customer_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        customer_form = CustomerForm()
        # Render the template depending on the context.
    return render(request,
                    'INKLined_app/customer_signup.html',
                    context = {'customer_form': customer_form,
                               'registered': registered})

def register_artist(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        artist_form = ArtistForm(request.POST)
        choice = artist_form['STYLE_1']
        
        #profile_form = UserProfileForm(request.POST)
        # If the two forms are valid...
        if artist_form.is_valid():
            # Save the user's form data to the database.            
            artist = artist_form.save()
            # Now we hash the PASSWORD with the set_PASSWORD method.
            # Once hashed, we can update the user object.
            user = User.objects.get_or_create(username=artist.ARTIST_USERNAME,password=artist.PASSWORD)[0]
            user.set_password(artist.PASSWORD)
            user.save()
            
            if 'PROFILE_PICTURE' in request.FILES:
                artist.PROFILE_PICTURE =  request.FILES['PROFILE_PICTURE']
            else:
                artist.PROFILE_PICTURE =  'profile_images/user.png'
                
            artist.save()

            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(artist_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        artist_form = ArtistForm()
        # Render the template depending on the context.
    return render(request,
                    'INKLined_app/artist_signup.html',
                    context = {'artist_form': artist_form,
                               'registered': registered})






                                            


    

