from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Customer
from rango.models import Artist
from rango.models import Review
#from rango.forms import CategoryForm
#from rango.forms import UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
#from rango.forms import PageForm
from datetime import datetime

def index(request):
    #category_list = Category.objects.order_by('-likes')[:5]
    #pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    #context_dict['categories'] = category_list
    #context_dict['pages'] = pages_list

    visitor_cookie_handler(request)

    response = render(request, 'rango/index.html', context=context_dict)
    return response

def about(request):
    context_dict = {'boldmessage': 'Liam Davis'}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    
    return render(request, 'rango/about.html', context=context_dict)

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
        reviews = Review.objects.filter(ARTIST_USERNAME = ARTIST_USERNAME)
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
        context_dict['review'] = None
    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context=context_dict)

def add_artist(request):
    
    if not request.user.is_authenticated:
        return redirect('rango:login')
    
    form = ArtistForm()

    if request.method == 'POST':
        form = ArtistForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)
    return render(request, 'rango/add_artist.html', {'form': form})

def add_review(request, ARTIST_USERNAME):
    
    if not request.user.is_authenticated:
        return redirect('rango:login')
    
    try:
        artist = Artist.objects.get(ARTIST_USERNAME=ARTIST_USERNAME)
    except:
        artist = None
        
    if artist is None:
        return redirect('/rango/')
    
    form = PageForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            if artist:
                review = form.save(commit=False)
                review.ARTIST_USERNAME = artist.ARTIST_USERNAME
                review.save()
                
                return redirect(reverse('rango:show_artist',kwargs ={'ARTIST_USERNAME': ARTIST_USERNAME}))
            
        else:
            print(form.errors)
    context_dict = {'form': form, 'artist': artist}
    return render(request, 'rango/add_page.html', context=context_dict)



##def register(request):
##    # A boolean value for telling the template
##    # whether the registration was successful.
##    # Set to False initially. Code changes value to
##    # True when registration succeeds.
##    registered = False
##    # If it's a HTTP POST, we're interested in processing form data.
##    if request.method == 'POST':
##        # Attempt to grab information from the raw form information.
##        # Note that we make use of both UserForm and UserProfileForm.
##        user_form = UserForm(request.POST)
##        profile_form = UserProfileForm(request.POST)
##        # If the two forms are valid...
##        if user_form.is_valid() and profile_form.is_valid():
##            # Save the user's form data to the database.
##            user = user_form.save()
##            # Now we hash the password with the set_password method.
##            # Once hashed, we can update the user object.
##            user.set_password(user.password)
##            user.save()
##            # Now sort out the UserProfile instance.
##            # Since we need to set the user attribute ourselves,
##            # we set commit=False. This delays saving the model
##            # until we're ready to avoid integrity problems.
##            profile = profile_form.save(commit=False)
##            profile.user = user
##            # Did the user provide a profile picture?
##            # If so, we need to get it from the input form and
##            #put it in the UserProfile model.
##            if 'picture' in request.FILES:
##                profile.picture = request.FILES['picture']
##            # Now we save the UserProfile model instance.
##            profile.save()
##            # Update our variable to indicate that the template
##            # registration was successful.
##            registered = True
##        else:
##            # Invalid form or forms - mistakes or something else?
##            # Print problems to the terminal.
##            print(user_form.errors, profile_form.errors)
##    else:
##        # Not a HTTP POST, so we render our form using two ModelForm instances.
##        # These forms will be blank, ready for user input.
##        user_form = UserForm()
##        profile_form = UserProfileForm()
##        # Render the template depending on the context.
##    return render(request,
##                    'rango/register.html',
##                    context = {'user_form': user_form,
##                               'profile_form': profile_form,
##                               'registered': registered})
##
##
##
##def user_login(request):
##    if request.method == 'POST':
##        username = request.POST.get('username')
##        password = request.POST.get('password')
##
##        user = authenticate(username=username, password=password)
##
##        if user:
##            if user.is_active:
##                login(request,user)
##                return redirect(reverse('rango:index'))
##            else:
##                return HttpResponse("Your Rango account is disabled.")
##        else:
##            print(f"Invalid login details: {username}, {password}")
##            return HttpResponse("Invalid login details supplied.")
##    else:
##        return render(request, 'rango/login.html')
##
##
##@login_required
##def restricted(request):
##    return render(request, 'rango/restricted.html')
##
##             
##@login_required
##def user_logout(request):
##    logout(request)
##    return redirect(reverse('rango:index'))
##
##def get_server_side_cookie(request, cookie, default_val=None):
##    val = request.session.get(cookie)
##    if not val:
##        val = default_val
##    return val
##
### Updated the function definition
##def visitor_cookie_handler(request):
##    visits = int(get_server_side_cookie(request, 'visits', '1'))
##    last_visit_cookie = get_server_side_cookie(request,
##                                               'last_visit',
##                                               str(datetime.now()))
##    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
##                                        '%Y-%m-%d %H:%M:%S')
##    
##    # If it's been more than a day since the last visit...
##    if (datetime.now() - last_visit_time).days > 0:
##        visits = visits + 1
##        # Update the last visit cookie now that we have updated the count
##        request.session['last_visit'] = str(datetime.now())
##    else:
##        # Set the last visit cookie
##        request.session['last_visit'] = last_visit_cookie
##        
##    # Update/set the visits cookie
##    request.session['visits'] = visits

                                            


    

