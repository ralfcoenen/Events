from django.contrib import admin

from .models import Event, Teilnehmer

class TeilnehmerInline(admin.TabularInline):
   model = Teilnehmer
   extra = 3


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['bezeichnung']}),
        ('Von Bis',             {'fields': ['beginn','ende'], 'classes': ['ccollapse']}),

    ]
    inlines = [TeilnehmerInline]
    list_display = ('bezeichnung','beginn','ende')
    

admin.site.register(Event,EventAdmin)
#admin.site.register(Teilnehmer)
