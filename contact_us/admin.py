from django.contrib import admin

from contact_us.models import ContactUs, Feedback


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_per_page = 10
    date_hierarchy = 'created_at'
    list_display = ('id', 'full_name',
                    'email', 'subject')
    list_display_links = ('id', 'full_name', 'email',)
    search_fields = ('first_name', 'last_name', 'message',
                     'email', 'subject',)
    readonly_fields = ('created_at', 'updated_at',)

    @admin.display(description='Full Name')
    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_per_page = 10
    date_hierarchy = 'created_at'
    list_display = ('id',  'scientific_name', 'common_names',
                    'family', 'user', 'image_tag', 'verification_status', 'created_at')
    list_display_links = ('id', 'scientific_name',)
    list_filter = ('duration', 'growth_habit','is_verified')
    search_fields = ('common_names', 'description',
                     'medicinal_properties', 'family', 'genus', 'species')
    readonly_fields = ('created_at', 'updated_at',)

    @admin.display(description='Scientific Name')
    def scientific_name(self, obj):
        if obj.species is not None:
            return f'{obj.genus} {obj.species}'.strip()
        else:
            return f'{obj.genus}'
        
    @admin.display(description='Is verified')
    def verification_status(self, obj):
        if obj.is_verified == True:
            return 'Verified'
        else:
            return 'Not verified'

