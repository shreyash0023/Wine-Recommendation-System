from django.contrib import admin
from .models import * 
from import_export.admin import ImportExportModelAdmin, ImportExportMixinBase
#pip install django-import-export
# Register your models here.
@admin.register(Wine)
class ViewAdmin(ImportExportModelAdmin):
	pass

