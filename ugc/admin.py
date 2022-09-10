from django.contrib import admin

from .models import Profile, BotMessage, BotButton, Resume, WorkType, WorkTypeResume, Order


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'employee')


@admin.register(BotMessage)
class BotMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'text_eng')


@admin.register(BotButton)
class BotButtonAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'text_eng', 'status')


@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name', 'subtype_status', 'relates_to')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'status')


@admin.register(WorkTypeResume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'resume', 'work_type', 'content')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date')
