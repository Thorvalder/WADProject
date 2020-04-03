from django.test import TestCase
from INKLined_app.models import *
from INKLined_app.views import *
import pytest
from django.contrib.auth.models import User
from datetime import date
import os
from django.urls import reverse

@pytest.mark.django_db


class TestModels(TestCase):
    @classmethod
    #set up
    def setUpTestData(cls):
        Customer.objects.create(USERNAME='HOTDOG123',
         PASSWORD='12345',)
        Artist.objects.create(ARTIST_USERNAME='ekaterinaterzieva',
         PASSWORD='12345',
         ADDRESS='Glasgow,Hillhead street',
         FULL_NAME='Ekaterina Terzieva',
         CONTACT_DETAILS='ekaterinaterzieva@tattoo.com',
         STYLE_1='Nature',)
        

    def setUp(self):
        pass
    
    #test: customer's password label
    def test_label_cus_password(self):
        name = Customer.objects.get(id=1)
        field_label = name._meta.get_field('PASSWORD').verbose_name
        self.assertEqual(field_label, 'PASSWORD')
    
    #test: customer's password
    def test_cus_password(self):
        name = Customer.objects.get(USERNAME='HOTDOG123')
        self.assertEqual('12345', name.PASSWORD)
        
    #test: costumer can save artist
    def test_save_art(self):
        art=Artist.objects.get(ARTIST_USERNAME='ekaterinaterzieva')
        cus = Customer.objects.get(USERNAME='HOTDOG123')
        s = Saves(CUSTOMER=cus,ARTIST=art)
        s.save()
        self.assertEqual((s.CUSTOMER.USERNAME == 'HOTDOG123' and s.ARTIST.ARTIST_USERNAME== 'ekaterinaterzieva'), True)
        
    #test:  customer can add review
    def test_cus_add_rev(self):
        r = Review(PICTURE = 'PICTURE' ,CUSTOMER = Customer.objects.get(USERNAME='HOTDOG123'),ARTIST = Artist.objects.get(ARTIST_USERNAME='ekaterinaterzieva'),TITLE = 'TITLE',
               DESCRIPTION = 'DESCRIPTION' ,RATING = 5,DATE = date.today())
        r.save()
        self.assertEqual((r.CUSTOMER.USERNAME== 'HOTDOG123'), True)
    
    #test: review is added to artist's reviews
    def test_review_added_to_artist(self):
        r = Review(PICTURE = 'PICTURE' ,CUSTOMER = Customer.objects.get(USERNAME='HOTDOG123'),ARTIST = Artist.objects.get(ARTIST_USERNAME='ekaterinaterzieva'),TITLE = 'TITLE',
               DESCRIPTION = 'DESCRIPTION' ,RATING = 5,DATE = date.today())
        r.save()
        ARTIST = Artist.objects.get(ARTIST_USERNAME='ekaterinaterzieva')
        reviews=Review.objects.filter(ARTIST=ARTIST)
        self.assertEqual(len(reviews),1)
    
    #test: artist can add a oicture
    def test_add_pic(self):
        p = Picture(ARTIST=Artist.objects.get(ARTIST_USERNAME='ekaterinaterzieva'),UPLOADED_IMAGE='UPLOADED_IMAGE')
        p.save()
        self.assertEqual((p.ARTIST.ARTIST_USERNAME== 'ekaterinaterzieva'), True)
 
    #Views tests
class index_View_Tests(TestCase):
    def setUp(self):
       self.response = self.client.get(reverse('index'))
       self.content = self.response.content.decode()

    def test_template(self):
       self.assertTemplateUsed(self.response, 'INKLined_app/base.html')

class sign_up_View_Tests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('INKLined_app:sign_up'))
        self.content = self.response.content.decode()

    def test_template(self):
        self.assertTemplateUsed(self.response, 'INKLined_app/sign-up.html')

class login_View_Tests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('INKLined_app:login'))
        self.content = self.response.content.decode()

    def test_template(self):
        self.assertTemplateUsed(self.response, 'INKLined_app/login.html')
        
class home_View_Tests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('INKLined_app:home'))
        self.content = self.response.content.decode()

    def test_template(self):
        self.assertTemplateUsed(self.response, 'INKLined_app/home.html')


class artists_View_Tests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('INKLined_app:artists'))
        self.content = self.response.content.decode()

    def test_template(self):
        self.assertTemplateUsed(self.response, 'INKLined_app/artists.html')

        