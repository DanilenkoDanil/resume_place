from django.contrib import admin

from .forms import ProfileForm, ServiceForm
from .models import Profile, UsersMessage, BotMessage, BotButton, Orders, Service


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'balance', 'referral_count', 'referral_balance', 'ref', 'status')
    form = ProfileForm 


@admin.register(UsersMessage)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at')


@admin.register(BotMessage)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'button', 'text')


@admin.register(BotButton)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'text', 'status')


@admin.register(Orders)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform', 'type', 'service', 'count', 'user', 'status')


@admin.register(Service)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('platform', 'type', 'service', 'product_id', 'price', 'min_count', 'max_count', 'link_form')
    form = ServiceForm
