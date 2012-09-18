from django.contrib import admin

from models import Poll, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class PollAdmin(admin.ModelAdmin):
    inlines = (ChoiceInline,)

admin.site.register(Poll, PollAdmin)
