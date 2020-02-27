import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')
import django 
django.setup()
from rango.models import Customer, Review, Artist
from datetime import date

def populate(): 
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.
##    python_pages = [
##        {'title': 'Official Python Tutorial',
##         'url':'http://docs.python.org/3/tutorial/',
##        'views':60},
##        {'title':'How to Think like a Computer Scientist',
##         'url':'http://www.greenteapress.com/thinkpython/',
##         'views':40},
##        {'title':'Learn Python in 10 Minutes',
##         'url':'http://www.korokithakis.net/tutorials/python/',
##         'views':28}]
##
##    django_pages = [
##        {'title':'Official Django Tutorial',
##         'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
##         'views':30},
##        {'title':'Django Rocks',
##         'url':'http://www.djangorocks.com/',
##         'views':20},
##        {'title':'How to Tango with Django',
##         'url':'http://www.tangowithdjango.com/',
##         'views':14}]
##
##    other_pages = [
##        {'title':'Bottle',
##         'url':'http://bottlepy.org/docs/dev/',
##         'views':20},
##        {'title':'Flask',
##         'url':'http://flask.pocoo.org',
##         'views':12}]

    

##    cats = {'Python': {'pages': python_pages,
##                       'views' :128,
##                       'likes':64},
##            'Django': {'pages': django_pages,
##                       'views' :64,
##                       'likes':32},
##            'Other Frameworks': {'pages': other_pages,
##                                 'views' :32,
##                                 'likes':16}}

    arts=[
        {'ARTIST_USERNAME':'JDOE123',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,The Mitchell Library',
         'FULL_NAME':'John Doe',
         'CONTACT_DETAILS':'JDOE123@tattoo.com',
         'STYLE':1,
        },
        {'ARTIST_USERNAME':'JDOE456',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,SEC Centre',
         'FULL_NAME':'Jane Doe',
         'CONTACT_DETAILS':'JDOE456@tattoo.com',
         'STYLE':2,
        },
        {'ARTIST_USERNAME':'MJAK789',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,Hunterian Art Gallery',
         'FULL_NAME':'Mark Jackson',
         'CONTACT_DETAILS':'MJAK789@tattoo.com',
         'STYLE':3,
        },
        {'ARTIST_USERNAME':'FNIE123',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,University of Glasgow',
         'FULL_NAME':'Fraser Niel',
         'CONTACT_DETAILS':'FNIE123@tattoo.com',
         'STYLE':4,
        },
        {'ARTIST_USERNAME':'ZPET456',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,Hilton Glasgow Grosvenor',
         'FULL_NAME':'Zak Peters',
         'CONTACT_DETAILS':'ZPET456@tattoo.com',
         'STYLE':5,
        },
        {'ARTIST_USERNAME':'MJOH789',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,West End Post Office',
         'FULL_NAME':'Max Johns',
         'CONTACT_DETAILS':'MJOH789@tattoo.com',
         'STYLE':6,
        },
        {'ARTIST_USERNAME':'ESUE123',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,Bard in the Botanics',
         'FULL_NAME':'Emily Susser',
         'CONTACT_DETAILS':'ESUE123@tattoo.com',
         'STYLE':7,
        },
        {'ARTIST_USERNAME':'SSAM456',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,Glasgow Club Kelvin Hall',
         'FULL_NAME':'Sam Samson',
         'CONTACT_DETAILS':'SSAM456@tattoo.com',
         'STYLE':8,
        },
        {'ARTIST_USERNAME':'JHAM789',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,Glasgow University Union',
         'FULL_NAME':'Jack Hammer',
         'CONTACT_DETAILS':'JHAM789@tattoo.com',
         'STYLE':9,
        },
        {'ARTIST_USERNAME':'BDOV123',
         'PASSWORD':'12345',
         'ADDRESS':'Glasgow,University of Glasgow Gift Shop',
         'FULL_NAME':'Ben Dover',
         'CONTACT_DETAILS':'BDOV123@tattoo.com',
         'STYLE':10,
        }]

    revs = [
        {
         'ARTIST':arts[0],
         'PICTURE':'nature-tattoo.jpg',
         'TITLE':'My new flower tattoo!',
         'DESCRIPTION':'Got this last week and I love it. Tulips are the best!',
         'RATING':4,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[1],
         'PICTURE':'cartoon-tattoo.jpeg',
         'TITLE':'My new cartoon tattoo!',
         'DESCRIPTION':'Got this last week and I like it. Disney is the best!',
         'RATING':3,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[2],
         'PICTURE':'abstract-tattoo.jpg',
         'TITLE':'My new abstract tattoo!',
         'DESCRIPTION':'Got this last week and I love it. Abstract is the best!',
         'RATING':5,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[3],
         'PICTURE':'geometric-tattoo.jpeg',
         'TITLE':'My new geometric tattoo!',
         'DESCRIPTION':'Got this last week and I hate it. Shapes are the best!',
         'RATING':1,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[4],
         'PICTURE':'realism-tattoo.jpg',
         'TITLE':'My new realism tattoo!',
         'DESCRIPTION':'Got this last week and I like it. Real is the best!',
         'RATING':3,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[5],
         'PICTURE':'tribal-tattoo.jpg',
         'TITLE':'My new tribal tattoo!',
         'DESCRIPTION':'Got this last week and I dislike it. Tribes are the best!',
         'RATING':2,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[6],
         'PICTURE':'sleave-tattoo.jpg',
         'TITLE':'My new sleave tattoo!',
         'DESCRIPTION':'Got this last week and I like it. Arms are the best!',
         'RATING':4,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[7],
         'PICTURE':'Tesco-tattoo.jpg',
         'TITLE':'My new writing tattoo!',
         'DESCRIPTION':'Got this last week and I love it. Tesco is the best!',
         'RATING':5,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[8],
         'PICTURE':'non-english-tattoo.jpg',
         'TITLE':'My new chinese tattoo!',
         'DESCRIPTION':'Got this last week and I like it. China is the best!',
         'RATING':4,
         'DATE':date.today()
        },
        {
         'ARTIST':arts[9],
         'PICTURE':'other-tattoo.jpg',
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


    
    

##    for cat, cat_data in cats.items():
##        c = add_cat(cat,cat_data['views'],cat_data['likes'])
##        for p in cat_data['pages']:
##            add_page(c, p['title'], p['url'],p['views'])
##            
##    # Print out the categories we have added.
##    for c in Category.objects.all():
##        for p in Page.objects.filter(category=c):
##            print(f'- {c}: {p}')

    for cust in custs:
        add_cus(cust['USERNAME'],cust['PASSWORD'],cust.get('PROFILE_PICTURE','none'))

    counter = 0

    for art in arts:
        add_art(art['ARTIST_USERNAME'],art['PASSWORD'],art['ADDRESS'],art.get('PROFILE_PICTURE','none'),art['FULL_NAME'],art['CONTACT_DETAILS'],art['STYLE'])

    for rev in revs:
        add_rev(Artist.objects.get(ARTIST_USERNAME = rev['ARTIST']['ARTIST_USERNAME']),Customer.objects.get(USERNAME = custs[counter]['USERNAME']),rev['PICTURE'],rev['TITLE'],rev['DESCRIPTION'],rev['RATING'],rev['DATE'])
        counter+=1
        if(counter == 5):
            counter = 0
        

def add_art(ARTIST_USERNAME,PASSWORD,ADDRESS,PROFILE_PICTURE,FULL_NAME,CONTACT_DETAILS,STYLE):
    a = Artist.objects.get_or_create(ARTIST_USERNAME=ARTIST_USERNAME)[0]
    a.PASSWORD = PASSWORD
    a.ADDRESS = ADDRESS
    
    if(PROFILE_PICTURE != 'none'):
        a.PROFILE_PICTURE = PROFILE_PICTURE
        
    a.FULL_NAME = FULL_NAME
    a.CONTACT_DETAILS = CONTACT_DETAILS
    a.STYLE = STYLE
    a.save()
    return a

def add_cus(USERNAME,PASSWORD,PROFILE_PICTURE):
    c = Customer.objects.get_or_create(USERNAME=USERNAME)[0]
    c.PASSWORD = PASSWORD
    if(PROFILE_PICTURE != 'none'):
        c.PROFILE_PICTURE = PROFILE_PICTURE
    c.save()
    return c

def add_rev(a,c, PICTURE, TITLE,DESCRIPTION,RATING,DATE):
    r = Review(PICTURE = PICTURE,CUSTOMER = c,ARTIST = a,TITLE = TITLE,
               DESCRIPTION = DESCRIPTION,RATING = RATING,DATE = DATE)
##    r.PICTURE = PICTURE
##    r.USERNAME = USERNAME
##    r.CUSTOMER = c
##    r.ARTIST = a
##    r.TITLE = TITLE
##    r.DESCRIPTION = DESCRIPTION
##    r.RATING = RATING
##    r.DATE = DATE
    r.save()
    temp = a.TOTAL_REVIEWS
    a.TOTAL_REVIEWS += 1
    if(type(a.RATING) != type(int)):
        a.RATING = 0
    a.RATING = ((a.RATING*temp)+RATING)/a.TOTAL_REVIEWS
    a.save()
    
    
    return r

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()


