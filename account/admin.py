from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'fullname', 'country',
        'email', 'is_verified', 'is_staff', 'is_superuser', 'created_at', 'updated_at', 'last_login',
    )
    list_display_links = ('id', 'fullname',)
    list_filter = ('country', 'is_verified', 'is_active', 'is_staff',)
    search_fields = ('first_name', 'last_name', 'email', 'contact',)

    readonly_fields = ('password', 'last_login',
                       'created_at', 'updated_at')

    @admin.display(description='Name')
    def fullname(self, obj):
        return f'{obj.first_name} {obj.last_name}'.strip()
