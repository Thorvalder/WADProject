#Importing relevant files and setting up django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'INKLined_project.settings')
import django 
django.setup()
from INKLined_app.models import Customer, Review, Artist,Picture,Saves
from django.contrib.auth.models import User
from datetime import date
from random import randint

def populate(): 
    #Setting up dictionaries with artist, review and custome details

    arts=[
        {'ARTIST_USERNAME':'JDOE123',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,The Mitchell Library',
         'FULL_NAME':'John Doe',
         'CONTACT_DETAILS':'JDOE123@tattoo.com',
         'STYLE_1':'Nature',
        },
        {'ARTIST_USERNAME':'JDOE456',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,SEC Centre',
         'FULL_NAME':'Jane Doe',
         'CONTACT_DETAILS':'JDOE456@tattoo.com',
         'STYLE_1':'Cartoon',
        },
        {'ARTIST_USERNAME':'MJAK789',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,Hunterian Art Gallery',
         'FULL_NAME':'Mark Jackson',
         'CONTACT_DETAILS':'MJAK789@tattoo.com',
         'STYLE_1':'Abstract',
        },
        {'ARTIST_USERNAME':'FNIE123',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,University of Glasgow',
         'FULL_NAME':'Fraser Niel',
         'CONTACT_DETAILS':'FNIE123@tattoo.com',
         'STYLE_1':'Geometric',
        },
        {'ARTIST_USERNAME':'ZPET456',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,Hilton Glasgow Grosvenor',
         'FULL_NAME':'Zak Peters',
         'CONTACT_DETAILS':'ZPET456@tattoo.com',
         'STYLE_1':'Realism',
        },
        {'ARTIST_USERNAME':'MJOH789',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,West End Post Office',
         'FULL_NAME':'Max Johns',
         'CONTACT_DETAILS':'MJOH789@tattoo.com',
         'STYLE_1':'Tribal',
        },
        {'ARTIST_USERNAME':'ESUE123',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,Bard in the Botanics',
         'FULL_NAME':'Emily Susser',
         'CONTACT_DETAILS':'ESUE123@tattoo.com',
         'STYLE_1':'Sleave',
        },
        {'ARTIST_USERNAME':'SSAM456',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,Glasgow Club Kelvin Hall',
         'FULL_NAME':'Sam Samson',
         'CONTACT_DETAILS':'SSAM456@tattoo.com',
         'STYLE_1':'Writing',
        },
        {'ARTIST_USERNAME':'JHAM789',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,Glasgow University Union',
         'FULL_NAME':'Jack Hammer',
         'CONTACT_DETAILS':'JHAM789@tattoo.com',
         'STYLE_1':'Non-english Writing',
        },
        {'ARTIST_USERNAME':'BDOV123',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,University of Glasgow Gift Shop',
         'FULL_NAME':'Ben Dover',
         'CONTACT_DETAILS':'BDOV123@tattoo.com',
         'STYLE_1':'Other',
        }]

    revs = [
        {
         'ARTIST':arts[0],
         'PICTURE':'review_images/nature-tattoo.jpg',
         'TITLE':'My new flower tattoo!',
         'DESCRIPTION':'Got this last week and I love it. Tulips are the best!',
         'RATING':4,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[1],
         'PICTURE':'review_images/cartoon-tattoo.jpeg',
         'TITLE':'My new cartoon tattoo!',
         'DESCRIPTION':'Got this last week and I like it. Disney is the best!',
         'RATING':3,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[2],
         'PICTURE':'review_images/abstract-tattoo.jpg',
         'TITLE':'My new abstract tattoo!',
         'DESCRIPTION':'Got this last week and I love it. Abstract is the best!',
         'RATING':5,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[3],
         'PICTURE':'review_images/geometric-tattoo.jpeg',
         'TITLE':'My new geometric tattoo!',
         'DESCRIPTION':'Got this last week and I hate it. Shapes are the best!',
         'RATING':1,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[4],
         'PICTURE':'review_images/realism-tattoo.jpg',
         'TITLE':'My new realism tattoo!',
         'DESCRIPTION':'Got this last week and I like it. Real is the best!',
         'RATING':3,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[5],
         'PICTURE':'review_images/tribal-tattoo.jpg',
         'TITLE':'My new tribal tattoo!',
         'DESCRIPTION':'Got this last week and I dislike it. Tribes are the best!',
         'RATING':2,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[6],
         'PICTURE':'review_images/sleave-tattoo.jpg',
         'TITLE':'My new sleave tattoo!',
         'DESCRIPTION':'Got this last week and I like it. Arms are the best!',
         'RATING':4,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[7],
         'PICTURE':'review_images/Tesco-tattoo.jpg',
         'TITLE':'My new writing tattoo!',
         'DESCRIPTION':'Got this last week and I love it. Tesco is the best!',
         'RATING':5,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[8],
         'PICTURE':'review_images/non-english-tattoo.jpg',
         'TITLE':'My new chinese tattoo!',
         'DESCRIPTION':'Got this last week and I like it. China is the best!',
         'RATING':4,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[9],
         'PICTURE':'review_images/other-tattoo.jpg',
         'TITLE':'My new sword tattoo!',
         'DESCRIPTION':'Got this last week and I like it. Weapons are the best!',
         'RATING':3,
         'DATE':date.today()
        },
    ]

    custs = [
        {'USERNAME':'HOTDOG123',
         'PASSWORD':'12345',
         },
        {'USERNAME':'COOLCAT456',
         'PASSWORD':'12345',
         },
        {'USERNAME':'WARMTURTLE789',
         'PASSWORD':'12345',
         },
        {'USERNAME':'BOILINGPARROT123',
         'PASSWORD':'12345',
         },
        {'USERNAME':'FROZENHAMSTER456',
         'PASSWORD':'12345',
         },
        ]


    
    #adding artist, customers, pictures,saves and reviews to the database
    for art in arts:
        add_art(art['ARTIST_USERNAME'],art['PASSWORD'],art['ADDRESS'],art.get('PROFILE_PICTURE','none'),art['FULL_NAME'],art['CONTACT_DETAILS'],art['STYLE_1'])

    for cust in custs:
        add_cus(cust['USERNAME'],cust['PASSWORD'],cust.get('PROFILE_PICTURE','none'))

    for art in arts:
        add_pic(Artist.objects.get(ARTIST_USERNAME = art['ARTIST_USERNAME']),'artist_images/INKLined_logo.jpg')

    for cust in custs:
        ca = randint(0,len(arts)-1)
        add_sav(Customer.objects.get(USERNAME = cust['USERNAME']),Artist.objects.get(ARTIST_USERNAME =arts[ca]['ARTIST_USERNAME']))
        
        

    counter = 0


    for rev in revs:
        add_rev(Artist.objects.get(ARTIST_USERNAME = rev['ARTIST']['ARTIST_USERNAME']),Customer.objects.get(USERNAME = custs[counter]['USERNAME']),rev['PICTURE'],rev['TITLE'],rev['DESCRIPTION'],rev['RATING'],rev['DATE'])
        counter+=1
        if(counter == 5):
            counter = 0
        
#method for creating artists
def add_art(ARTIST_USERNAME,PASSWORD,ADDRESS,PROFILE_PICTURE,FULL_NAME,CONTACT_DETAILS,STYLE):
    #creates a new artist, giving them a default profile picture if one wasn't assigned
    a = Artist.objects.get_or_create(ARTIST_USERNAME=ARTIST_USERNAME)[0]
    a.PASSWORD = PASSWORD
    a.ADDRESS = ADDRESS
    
    if(PROFILE_PICTURE != 'none'):
        a.PROFILE_PICTURE = PROFILE_PICTURE
    else:
        a.PROFILE_PICTURE = 'profile_images/user.png'
        
    a.FULL_NAME = FULL_NAME
    a.CONTACT_DETAILS = CONTACT_DETAILS
    a.STYLE_1 = STYLE
    #adds the artist to the database
    a.save()
    #creates a new user object with the artist username and password for authentication purposes
    user = User.objects.get_or_create(username=a.ARTIST_USERNAME,password=a.PASSWORD)[0]
    #hashing the password of the user so that it is encrypted
    user.set_password(PASSWORD)
    #adding the user to the database
    user.save()
    #returns the artist
    return a

#method for adding new customers
def add_cus(USERNAME,PASSWORD,PROFILE_PICTURE):
    #creates a new customer object and gives it a default profile picture if one wasn't assigned
    c = Customer.objects.get_or_create(USERNAME=USERNAME)[0]
    c.PASSWORD = PASSWORD
    if(PROFILE_PICTURE != 'none'):
        c.PROFILE_PICTURE = PROFILE_PICTURE
    else:
        c.PROFILE_PICTURE = 'profile_images/user.png'

    #adds the customer to the database
    c.save()
    #creates a new user object with the customer username and password for authentication purposes
    user = User.objects.get_or_create(username=c.USERNAME,password=c.PASSWORD)[0]
    #hashing the password of the user so that it is encrypted
    user.set_password(PASSWORD)
    #adding the user to the database
    user.save()
    #returns the customer
    return c

#method for adding reviews
def add_rev(a,c, PICTURE, TITLE,DESCRIPTION,RATING,DATE):
    #creates a new review with given details
    r = Review(PICTURE = PICTURE,CUSTOMER = c,ARTIST = a,TITLE = TITLE,
               DESCRIPTION = DESCRIPTION,RATING = RATING,DATE = DATE)

    #saves the review
    r.save()

    #calculates the artist's rating and total number of reviews
    temp = a.TOTAL_REVIEWS
    a.TOTAL_REVIEWS += 1
    if(type(a.RATING) != type(int)):
        a.RATING = 0
    a.RATING = ((a.RATING*temp)+RATING)/a.TOTAL_REVIEWS

    #updates the artist's rating and review number
    a.save()
    #returns the review
    return r

#method for adding pictures
def add_pic(a,UPLOADED_IMAGE):
    #creates a new picture using given details
    p = Picture(ARTIST=a,UPLOADED_IMAGE=UPLOADED_IMAGE)
    #adds the picture to the database
    p.save()
    #returns the picture
    return p

#method for adding a new customer save
def add_sav(c,a):
    #creates the new save using customer details and adds it to the database
    p = Saves(CUSTOMER=c,ARTIST=a)
    p.save()
    #returns the save
    return p




#Executes populate method when script is ran
if __name__ == '__main__':
    print('Starting INKLined_app population script...')
    populate()


