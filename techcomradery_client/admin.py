from django.contrib import admin
from .models import SocialMediaUser, SubscriptionUser


class SocialMediaUserAdmin(admin.ModelAdmin):
    list_display = ["social_media", "user", "social_media_id", "image_url", 'id']
    ordering = ["id"]


class SubscriptionUserAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "whatsapp", "linkedin", 'providing', 'referral', 'referred_by']


admin.site.register(SocialMediaUser, SocialMediaUserAdmin)
admin.site.register(SubscriptionUser, SubscriptionUserAdmin)
