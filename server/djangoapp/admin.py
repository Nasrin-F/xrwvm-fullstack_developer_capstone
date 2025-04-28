from django.contrib import admin
from .models import CarMake, CarModel

# Inline class for CarModel
class CarModelInline(admin.TabularInline):  # Use `TabularInline` for a simple tabular display
    model = CarModel
    extra = 1  # Number of empty forms to display initially
    fields = ('name', 'type', 'year')  # Fields to be shown in the inline form

# Admin class for CarMake
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Columns to show in the list view
    search_fields = ('name',)  # Make the name field searchable
    inlines = [CarModelInline]  # Add the inline for CarModel here

# Admin class for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year')  # Display these fields in the CarModel list view
    list_filter = ('car_make', 'type')  # Filters to show in the sidebar
    search_fields = ('name',)  # Make the name field searchable

# Register the models with custom admin views
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
