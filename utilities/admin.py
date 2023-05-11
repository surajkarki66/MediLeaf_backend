from django.contrib import admin


class UserStampModelAdmin(admin.ModelAdmin):
   readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')
   
   def save_model(self, request, obj, form, change):
      if not change:
         obj.created_by = request.user
      if change:
         obj.updated_by = request.user
      return super().save_model(request, obj, form, change)


class ReadonlyModelAdmin(admin.ModelAdmin):
   def has_add_permission(self, request, obj = None):
      return False
   def has_delete_permission(self, request, obj = None):
      return False
   def has_change_permission(self, request, obj = None):
      return False