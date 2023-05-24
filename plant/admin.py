from django.contrib import admin

from .models import Plant, PlantFamily, PlantGenus, PlantSpecies, PlantImage

class PlantImageInline(admin.StackedInline):
    model = PlantImage
    extra = 0
    max_num = 5
    formset_required = True

@admin.register(PlantSpecies)
class PlantSpeciesAdmin(admin.ModelAdmin):
    list_per_page = 10
    date_hierarchy = 'created_at'
    list_display = ('id', 'title', 'slug', 'genus', 'created_at', 'updated_at')
    list_display_links = (
        'id', 'title'
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'genus__title')
    readonly_fields = ('created_at', 'updated_at', 'slug')


@admin.register(PlantGenus)
class PlantGenusAdmin(admin.ModelAdmin):
    list_per_page = 10
    date_hierarchy = 'created_at'
    list_display = ('id', 'title', 'slug', 'family',
                    'created_at', 'updated_at')
    list_display_links = (
        'id', 'title'
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'family__title')
    readonly_fields = ('created_at', 'updated_at', 'slug')


@admin.register(PlantFamily)
class PlantFamilyAdmin(admin.ModelAdmin):
    list_per_page = 10
    date_hierarchy = 'created_at'
    list_display = ('id', 'title', 'slug', 'created_at', 'updated_at')
    list_display_links = (
        'id', 'title'
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', )
    readonly_fields = ('created_at', 'updated_at', 'slug')


@admin.register(PlantImage)
class PlantImageAdmin(admin.ModelAdmin):
    list_per_page = 10
    date_hierarchy = 'created_at'
    list_display = ('id', 'scientific_name', 'part', 'image_tag',
                    'default_status', 'created_at', 'updated_at',)
    list_display_links = ('id', 'scientific_name')
    list_filter = ('created_at', 'updated_at', 'part',
                   'plant__duration', 'plant__growth_habit')
    search_fields = ('plant__common_name', 'plant__common_name_ne',)
    readonly_fields = ('created_at', 'updated_at',)

    @admin.display(description='Default Status')
    def default_status(self, obj):
        if obj.default:
            return "Default"
        else:
            return "Not default"

    @admin.display(description='Scientific Name')
    def scientific_name(self, obj):
        return f'{obj.plant.genus} {obj.plant.species}'.strip()


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_per_page = 10
    date_hierarchy = 'created_at'
    list_display = ('id', 'family', 'scientific_name',
                    'common_name', 'common_name_ne', 'duration', 'growth_habit', 'default_image_tag')
    list_display_links = ('id', 'family',)
    list_filter = ('duration', 'growth_habit')
    search_fields = ('common_name', 'common_name_ne', 'description',
                     'description_ne', 'medicinal_properties', 'medicinal_properties_ne', 'family__title', 'genus__title', 'species__title')
    readonly_fields = ('created_at', 'updated_at', 'no_of_observations')

    @admin.display(description='Scientific Name')
    def scientific_name(self, obj):
        return f'{obj.genus} {obj.species}'.strip()

    inlines = (PlantImageInline,)
