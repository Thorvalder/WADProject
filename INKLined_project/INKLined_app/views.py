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
            #sends the user to their account page
            response = render(request, 'INKLined_app/my-account.html', context=context_dict)
            return response
            
        else:
            print(f"Invalid login details")
            #informs of incorrect login details
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
    # then it will send details to the context dictionary accordingly
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
    #sends the user to their account page
    return render(request, 'INKLined_app/my-account.html', context=context_dict)

#view for showing the customer their saved artists
def show_saved(request):
    #finds the customers username and gets all of the matching saves
    USERNAME = request.user.username
    context_dict = {}
    customer = Customer.objects.get(USERNAME = USERNAME)
    saves = Saves.objects.filter(CUSTOMER=customer)

    #fills context dictionary with customer details and their saved artists with one of the artist's pictures if they have any uploaded
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
    
    #sends the user to their saved artists page
    return render(request, 'INKLined_app/saved-artists.html', context=context_dict)

#view for showing the sign up page
def sign_up(request):
    context_dict = {}
    #Joseph added next line for CSS
    context_dict['pageIsSignUp']=True;

    #sends the user to the sign up page
    return render(request, 'INKLined_app/sign-up.html', context=context_dict)

#view for deleting accounts
def delete_account(request):
    #checks if the user is logged in and if not then sends them to the login page
    if request.user.is_authenticated:
        USERNAME = request.user.username
        USER = request.user
    else:
        return redirect(reverse('INKLined_app:login'))

    #logs out the user then deletes them from the user table
    logout(request)
    USER.delete()

    #deletes the user from their respective table
    try:
        customer = Customer.objects.get(USERNAME = USERNAME)
        customer.delete()
    except:
        ARTIST_USERNAME = USERNAME
        artist = Artist.objects.get(ARTIST_USERNAME = ARTIST_USERNAME)
        artist.delete()
    #sends the user to the home page
    return redirect(reverse('INKLined_app:index'))

#view for showing the list of artists
def artists(request):

    #gets all of the artist objects and sends them to the context dictionary with a picture from their gallery if they have one
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
    #sends the user to the list of artists page
    return render(request, 'INKLined_app/artists.html', context=context_dict)
    
#view for showing an artist's page
def show_artist(request, ARTIST_USERNAME):
    
    #Attempts to get the details of the artist
    
    context_dict = {}
    try:
        
        artist = Artist.objects.get(ARTIST_USERNAME = ARTIST_USERNAME)
        reviews = Review.objects.filter(ARTIST = artist)

        context_dict['reviews'] = reviews

        context_dict['artist'] = artist
        pictures=Picture.objects.filter(ARTIST=artist)
        context_dict['pictures'] = pictures
        context_dict['PROFILE_PICTURE'] = artist.PROFILE_PICTURE
        #specified string to be used to query by the embedded google maps search engine
        context_dict['gmaps_location'] = "https://www.google.com/maps/embed/v1/place?q="+artist.ADDRESS.replace(" ","+")+",+Glasgow,+UK&key=AIzaSyDrnqDTlBB6vGWaMmrb7zCkap09boRPslk"

        #checks to see if the user has already saved this artist
        try:
            usernameC = request.user.username
            customer = Customer.objects.get(USERNAME = usernameC)
            save = Saves.objects.get(CUSTOMER=customer,ARTIST=artist)
            context_dict['AlreadySaved'] = True
        except:
            context_dict['AlreadySaved'] = False

    #if artist is not found then the user is redirected to the artists page
    except Artist.DoesNotExist:

        context_dict['artist'] = None
        context_dict['reviews'] = None
        return render(request, 'INKLined_app/artists.html', context=context_dict)
    #checks to see if the user is a customer or artist and sends info to context dictionary
    try:
        USERNAME = request.user.username
        customer = Customer.objects.get(USERNAME = USERNAME)
        context_dict['USERTYPE'] = True
    except:
        context_dict['USERTYPE'] = False

    #sends the user to the artist's page
    return render(request, 'INKLined_app/ARTIST_USERNAME.html', context=context_dict)

#view for adding pictures to an artists gallery
def add_picture(request):

    #if the artist is not logged in send them to the login page
    if not request.user.is_authenticated:
        return redirect('INKLined_app:login')

    #if the request is coming from the form input then attempt to add the picture to the database
    if request.method == 'POST':
        
        picture_form = PictureForm(request.POST)
            
        # If the form is valid...
        if picture_form.is_valid():
            
            if 'UPLOADED_IMAGE' not in request.FILES:
                print("Must have picture")
                picture_form = PictureForm()
                artist = Artist.objects.get(ARTIST_USERNAME= request.user.username)
                return render(request,'INKLined_app/add_picture.html',context={'artist':artist,
                                                                      'picture_form':picture_form})
            # Save the picture data to the database.
            picture = picture_form.save(commit=False)
            picture.UPLOADED_IMAGE = request.FILES['UPLOADED_IMAGE']
            picture.ARTIST = Artist.objects.get(ARTIST_USERNAME= request.user.username)
            picture.save()
            #send the artist to their page
            return redirect(reverse('INKLined_app:show_artist',
                                    kwargs={'ARTIST_USERNAME':
                                            request.user.username}))
		

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(review_form.errors)
    else:
        # Not a HTTP POST so renders blank picture form
        
        picture_form = PictureForm()
        artist = Artist.objects.get(ARTIST_USERNAME= request.user.username)
        #send the user to the add_picture page
        return render(request,'INKLined_app/add_picture.html',context={'artist':artist,
                                                                      'picture_form':picture_form})

#view for showing an artist's reviews
def show_reviews(request, ARTIST_USERNAME):

    #gets the artist and all of their reviews and sends them to the context dictionary along with the type of user making request
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
    #sends the user to the review page
    return render(request, 'INKLined_app/reviews.html', context=context_dict)

#view for adding and removing artists to the customer's saved artists
def save_artist(request, ARTIST_USERNAME):
    #gets the customer details and the artist details and if the save already exists then it deletes it
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

    #gets artist details and sends them to the context dictionary and sends the user to the artist's page
    context_dict['reviews'] = reviews

    context_dict['artist'] = artist
    context_dict['gmaps_location'] = "https://www.google.com/maps/embed/v1/place?q="+artist.ADDRESS.replace(" ","+")+",+Glasgow,+UK&key=AIzaSyDrnqDTlBB6vGWaMmrb7zCkap09boRPslk"
    return redirect(reverse('INKLined_app:show_artist' , args=[artist]))

#view for adding new reviews
def add_review(request, ARTIST_USERNAME):

    #if user is not logged in them send them to login page
    if not request.user.is_authenticated:
        return redirect('INKLined_app:login')
    
    # A boolean value for telling the template
    # whether the review adding was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    reviewed = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        #takes the data from the review form
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
            #updates the artist's information
            if type(artist.RATING) == type(int):
                artist.RATING = int(((artist.RATING*artist.TOTAL_REVIEWS) + review.RATING)/(artist.TOTAL_REVIEWS+1))
                artist.TOTAL_REVIEWS += 1
            else:
                artist.RATING = review.RATING
                artist.TOTAL_REVIEWS = 1
            #updates the review and artist
            review.save()
            artist.save()
            #sends the user back to the artist's page
            return redirect(reverse('INKLined_app:show_artist',
                                    kwargs={'ARTIST_USERNAME':
                                            ARTIST_USERNAME}))
		

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(review_form.errors)
    else:
        # Not a HTTP POST, so renders blank review form
        review_form = ReviewForm()
        artist = Artist.objects.get(ARTIST_USERNAME= ARTIST_USERNAME)
        # sends the user to the review page and renders the template depending on the context.
        return render(request,'INKLined_app/add_review.html',context={'artist':artist,
                                                                      'review_form':review_form})
        


#view for creating a new customer
def register_customer(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        customer_form = CustomerForm(request.POST)
        #checks customer form is valid
        if customer_form.is_valid():
            # Save the customer's form data to the database.
            customer = customer_form.save()
            #Creates a user object with customer info with a hashed password
            user = User.objects.get_or_create(username=customer.USERNAME,password=customer.PASSWORD)[0]
            user.set_password(customer.PASSWORD)
            user.save()

            #gets the customer's profle image if they send one, otherwise set it to a default
            if 'PROFILE_PICTURE' in request.FILES:
                customer.PROFILE_PICTURE =  request.FILES['PROFILE_PICTURE']
            else:
                customer.PROFILE_PICTURE =  'profile_images/user.png'

            #updates the customer
            customer.save()

            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(customer_form.errors)
    else:
        # Not a HTTP POST, renders blank form
        customer_form = CustomerForm()
        # Render the template depending on the context and sends user to customer signup page
    return render(request,
                    'INKLined_app/customer_signup.html',
                    context = {'customer_form': customer_form,
                               'registered': registered})

#view for creating a new artist 
def register_artist(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        #takes informtation from the artist form
        artist_form = ArtistForm(request.POST)
        choice = artist_form['STYLE_1']
        
        # If the forms are valid...
        if artist_form.is_valid():
            # Save the artist's form data to database          
            artist = artist_form.save()
            # creates new user with artist's info and hashed password
            user = User.objects.get_or_create(username=artist.ARTIST_USERNAME,password=artist.PASSWORD)[0]
            user.set_password(artist.PASSWORD)
            user.save()
            #attempts to get profile picture and if one wasn't provided then it uses a default
            if 'PROFILE_PICTURE' in request.FILES:
                artist.PROFILE_PICTURE =  request.FILES['PROFILE_PICTURE']
            else:
                artist.PROFILE_PICTURE =  'profile_images/user.png'
            #update teh artist object
            artist.save()
            
            #updates the registered status
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(artist_form.errors)
    else:
        # Not a HTTP POST, so we renders blank form
        artist_form = ArtistForm()
        # Render the template depending on the context and sends user to artist signup page
    return render(request,
                    'INKLined_app/artist_signup.html',
                    context = {'artist_form': artist_form,
                               'registered': registered})






                                            


    

