from django.contrib import admin
from api.models import (
    Folder,
    Document,
    Topic
)
# Register your models here.

admin.site.register(Folder)
admin.site.register(Document)
admin.site.register(Topic)