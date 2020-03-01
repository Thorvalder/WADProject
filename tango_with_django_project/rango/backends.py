from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from rango.models import Customer,Artist

class Customer_Artist_Backend(ModelBackend):

    def authenticate(self, request, USERNAME, password,usertype):
        print("backend in use")
        user_id = USERNAME
        password = password
        print(password)
        if usertype == 'customer':
            try:
                customer = Customer.objects.get(USERNAME=user_id)
                print(customer.check_password(password))
                
                if customer.check_password(password) is True:
                    print(customer.USERNAME)
                    return customer
            except Exception as e:
                pass
        else:
            try:
                artist = Artist.objects.get(ARTIST_USERNAME=user_id)
                if artist.check_password(password) is True:
                    return artist
            except:
                pass

    def get_user(self, user_id):
        try:
            return Customer.objects.get(USERNAME=user_id)
        except Customer.DoesNotExist:
            try:
                return Artist.objects.get(ARTIST_USERNAME=user_id)
            except Artist.DoesNotExist:
                return None
