from django.contrib import admin
from myapp.models import UserProfile, Event, Connection, MarketPlace, Adgenda, AdgendaInvites, EventInvites, UploadIMG

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Connection)
admin.site.register(MarketPlace)
admin.site.register(AdgendaInvites)
admin.site.register(EventInvites)
admin.site.register(UploadIMG)
admin.site.register(Adgenda)
