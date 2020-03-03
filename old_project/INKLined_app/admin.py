from django.contrib import admin
from INKLined_app.models import Customer, Artist, Review,Picture,Saves
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomerChangeForm, CustomerForm,ArtistChangeForm,ArtistForm


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerChangeForm
    add_form = CustomerForm
    list_display = ('USERNAME','PASSWORD','PROFILE_PICTURE')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('USERNAME', 'PROFILE_PICTURE', 'password1', 'password2')}
         ),
    )
    search_fields = ('USERNAME',)
    ordering = ('USERNAME',)

class ArtistAdmin(admin.ModelAdmin):
    form = ArtistChangeForm
    add_form = ArtistForm
    list_display = ('ARTIST_USERNAME','PASSWORD','PROFILE_PICTURE','ADDRESS','RATING','TOTAL_REVIEWS','FULL_NAME','CONTACT_DETAILS','STYLE_1','STYLE_2','STYLE_3')
    
    

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('ARTIST_USERNAME', 'PROFILE_PICTURE', 'password1', 'password2','ADDRESS','FULL_NAME','CONTACT_DETAILS','STYLE_1','STYLE_2','STYLE_3')}
         
         ),
    )
    search_fields = ('ARTIST_USERNAME',)
    ordering = ('ARTIST_USERNAME',)

class PictureAdmin(admin.ModelAdmin):
    list_display = ('ID','ARTIST','UPLOADED_IMAGE')

class SavesAdmin(admin.ModelAdmin):
    list_display = ('CUSTOMER','ARTIST')
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ID','PICTURE','CUSTOMER','ARTIST','TITLE','DESCRIPTION','RATING','DATE')


admin.site.register(Review, ReviewAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Saves, SavesAdmin)

    
