from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'mail', 'verified_status', 'image_tag',)
    list_display_links = ('user', 'id',)
    list_filter = ('user__is_verified', )
    search_fields = ('user__first_name', 'user__last_name',
                     'user__contact', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'slug',)

    def mail(self, obj):
        return obj.user.email

    def verified_status(self, obj):
        return bool(obj.user.is_verified)
