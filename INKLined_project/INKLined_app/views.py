from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from INKLined_app.models import Customer,Artist,Review,Saves,Picture
from INKLined_app.forms import CustomerForm, ArtistForm, ReviewForm
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User
#from django.contrib.auth.hashers import set_password


def index(request):
    top_artist_list = Artist.objects.order_by('-RATING')[:5]
    context_dict = {}
    context_dict['top_artists'] = top_artist_list

    response = render(request, 'INKLined_app/home.html', context=context_dict)
    return response


def login_user(request):
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
                #context_dict['PASSWORD'] = user.get_password()
                context_dict['PROFILE_PICTURE'] = u.PROFILE_PICTURE
            else:
                u = Artist.objects.get(ARTIST_USERNAME=USERNAME)
                context_dict['ARTIST_USERNAME'] = u.ARTIST_USERNAME
                #context_dict['PASSWORD'] = user.get_password()
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



@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('INKLined_app:index'))


def show_account(request, USERNAME):
    context_dict = {}
    try:
        customer = Customer.objects.get(USERNAME = USERNAME)
        context_dict['account'] = customer
    except:
        try:
            artist = Artist.objects.get(ARTIST_USERNAME = USERNAME)
            context_dict['account'] = artist
        except:
            context_dict['account'] = None
            

    return render(request, 'INKLined_app/my-account.html', context=context_dict)


def show_saved(request):
    USERNAME = request.user.username
    context_dict = {}
    customer = Customer.objects.get(USERNAME = USERNAME)
    saves = Saves.objects.filter(CUSTOMER=customer)
    
    context_dict['account'] = customer
    context_dict['saves'] = saves
    print(saves)
    
    return render(request, 'INKLined_app/saved-artists.html', context=context_dict)

def sign_up(request):
    context_dict = {}
    #Joseph added next line for CSS
    context_dict['pageIsSignUp']=True;

    return render(request, 'INKLined_app/sign-up.html', context=context_dict)


def artists(request):
    
    context_dict = {}
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
    except Artist.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything
        # the template will display the "no category" message for us.
        context_dict['artist'] = None
        context_dict['reviews'] = None
        return render(request, 'INKLined_app/artists.html', context=context_dict)
    # Go render the response and return it to the client. +
    return render(request, 'INKLined_app/ARTIST_USERNAME.html', context=context_dict)

def add_picture(request):
    
    if not request.user.is_authenticated:
        return redirect('INKLined_app:login')
    
    form = PictureForm()

    if request.method == 'POST':
        form = PictureForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/INKLined_app/')
        else:
            print(form.errors)
    return render(request, 'INKLined_app/add_picture.html', {'form': form})


def show_reviews(request, ARTIST_USERNAME):
    artist = Artist.objects.get(ARTIST_USERNAME=ARTIST_USERNAME)
    reviews = Review.objects.filter(ARTIST=artist)
    context_dict = {'reviews':reviews}
    return render(request, 'INKLined_app/reviews.html', context=context_dict)




    
def add_review(request, ARTIST_USERNAME):
    
    if not request.user.is_authenticated:
        return redirect('INKLined_app:login')
    
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
        return redirect('/INKLined_app/')
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
    if form.is_valid():
        if customer and artist:
            review = form.save(commit=False)
            review.CUSTOMER = customer
            review.ARTIST = artist
            review.save()
            return redirect(reverse('INKLined_app:show_artist',
                                    kwargs={'ARTIST_USERNAME':
                                            ARTIST_USERNAME}))
    else:
        print(form.errors)

    context_dict = {'form': form, 'Customer': customer}
    return render(request, 'INKLined_app/add_review.html', context=context_dict)



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
                customer.PROFILE_PICTURE =  'profile_images/default.jpg'
                
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
                artist.PROFILE_PICTURE =  'profile_images/default.jpg'
                
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






                                            


    

