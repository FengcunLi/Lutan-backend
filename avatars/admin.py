from django.contrib import admin

from avatars.models import Avatar


class AvatarModelAdmin(admin.ModelAdmin):
    readonly_fields = ['width', 'height']


admin.site.register(Avatar, AvatarModelAdmin)
