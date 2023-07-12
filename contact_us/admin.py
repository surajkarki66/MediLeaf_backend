from django.contrib import admin

from contact_us.models import ContactUs

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_per_page = 10
    date_hierarchy = 'created_at'
    list_display = ('id', 'full_name',
                    'email', 'subject')
    list_display_links = ('id', 'full_name', 'email',)
    search_fields = ('first_name', 'last_name', 'description',
                     'email', 'subject',)
    readonly_fields = ('created_at', 'updated_at',)

    @admin.display(description='Full Name')
    def full_name(self, obj):
     return f'{obj.first_name} {obj.last_name}'
