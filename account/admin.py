from django.contrib import admin
from django.contrib.auth import get_user_model

from userprofile.models import Profile
from .forms import UserForm, UserCustomCreationForm

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_per_page = 10
    date_hierarchy = 'created_at'
    form = UserForm
    add_form = UserCustomCreationForm
    ordering = ('-created_at',)
    list_display = (
        'id', 'fullname', 'country',
        'email', 'is_verified', 'staff_status', 'superuser_status', 'has_profile', 'created_at', 'updated_at', 'last_login',
    )
    list_display_links = ('id', 'fullname',)
    list_filter = ('country', 'is_verified', 'is_active', 'is_staff',)
    search_fields = ('first_name', 'last_name', 'email', 'contact',)

    readonly_fields = ('password', 'last_login',
                       'created_at', 'updated_at',)

    @admin.display(description='Name')
    def fullname(self, obj):
        return f'{obj.first_name} {obj.last_name}'.strip()

    @admin.display(description='Staff', boolean=True)
    def staff_status(self, obj):
        """
        The function checks if an object has staff status.

        :param sef: The first parameter, "sef", is likely a typo and should be "self". It is a reference
        to the instance of the class that the method is being called on
        :param obj: The "obj" parameter is an object that is being passed into the "staff_status"
        function. The function is checking whether this object has a "is_staff" attribute and returning
        its value
        :return: a boolean value indicating whether the given object has staff status or not.
        """
        return obj.is_staff

    @admin.display(description='SuperUser', boolean=True)
    def superuser_status(self, obj):
        """
        This function returns a boolean value indicating whether the given object is a superuser or not.

        :param obj: The object being passed as an argument to the function. It is likely an instance of a
        user model or a related model that has a boolean field indicating whether the user is a superuser
        or not. The function returns the value of this boolean field for the given object
        :return: a boolean value indicating whether the given object has superuser status or not.
        """
        return obj.is_superuser

    @admin.display(description='Profile')
    def has_profile(self, obj):
        if hasattr(obj, 'profile'):
            return 'Yes'
        else:
            return 'No'

    inlines = (ProfileInline,)
