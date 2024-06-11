from django.contrib import admin

from . import models


@admin.register(models.DjangoProjectType)
class DjangoProjectTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "public")


@admin.register(models.DjangoProjectStatus)
class DjangoProjectStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "public")


@admin.register(models.ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active")


@admin.register(models.ServiceProviderContact)
class ServiceProviderContactAdmin(admin.ModelAdmin):
    list_display = ("id", "serviceprovider", "name", "email")
