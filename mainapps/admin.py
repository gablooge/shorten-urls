from django.contrib import admin
from solo.admin import SingletonModelAdmin

from mainapps.models import TemplateConfig

admin.site.register(TemplateConfig, SingletonModelAdmin)
