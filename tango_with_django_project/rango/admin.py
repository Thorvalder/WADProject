from django.contrib import admin
from rango.models import Customer, Artist, Review
from django.contrib import admin

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('USERNAME','PASSWORD','PROFILE_PICTURE')
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ID','PICTURE','CUSTOMER','ARTIST','TITLE','DESCRIPTION','RATING','DATE')


class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {'ARTIST_USERNAME':('ARTIST_USERNAME',)}

admin.site.register(Review, ReviewAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Customer, CustomerAdmin)

    
