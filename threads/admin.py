from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from threads.models import Thread


class ThreadAdmin(GuardedModelAdmin):
    search_fields = ('id',)


admin.site.register(Thread, ThreadAdmin)
