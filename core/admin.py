from django.contrib import admin
from .models import (
    Category, Product, PackagingFormat, Certification, B2BInquiry, BlogPost, SiteSettings, HeroMedia
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'slug')
    search_fields = ('name_en', 'name_fr')
    prepopulated_fields = {'slug': ('name_en',)}
    fieldsets = (
        ('Basic Information', {'fields': ('name_en', 'slug', 'image')}),
        ('Translations', {'fields': (
            'name_fr', 'slug_fr',
            'name_ar', 'slug_ar',
            'name_es', 'slug_es',
            'name_it', 'slug_it'
        )}),
        ('Descriptions', {'fields': (
            'description_en', 'description_fr', 'description_ar', 'description_es', 'description_it'
        )}),
    )


@admin.register(PackagingFormat)
class PackagingFormatAdmin(admin.ModelAdmin):
    list_display = ('name', 'volume')
    search_fields = ('name',)
    fieldsets = (
        ('General Info', {'fields': ('name', 'volume')}),
        ('Material Translations', {'fields': (
            'material_en', 'material_fr', 'material_ar', 'material_es', 'material_it'
        )}),
        ('Carton Logistics specs', {'fields': (
            'carton_specs_en', 'carton_specs_fr', 'carton_specs_ar', 'carton_specs_es', 'carton_specs_it'
        )}),
        ('Pallet Logistics specs', {'fields': (
            'pallet_specs_en', 'pallet_specs_fr', 'pallet_specs_ar', 'pallet_specs_es', 'pallet_specs_it'
        )}),
    )


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'icon')
    search_fields = ('code', 'name')
    fieldsets = (
        ('Core', {'fields': ('code', 'name', 'icon', 'theme_color')}),
        ('Subtitle Translations', {'fields': (
            'subtitle_en', 'subtitle_fr', 'subtitle_ar', 'subtitle_es', 'subtitle_it'
        )}),
        ('Description Translations', {'fields': (
            'description_en', 'description_fr', 'description_ar', 'description_es', 'description_it'
        )}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'category', 'is_premium', 'is_featured', 'acidity', 'created_at')
    list_filter = ('category', 'is_premium', 'is_featured', 'acidity')
    search_fields = ('name_en', 'name_fr', 'name_ar')
    prepopulated_fields = {'slug': ('name_en',)}
    filter_horizontal = ('packaging_formats', 'certifications')
    
    fieldsets = (
        ('Basic Information', {'fields': (
            'category', 'name_en', 'slug', 'image', 'is_premium', 'is_featured'
        )}),
        ('Name Translations', {'fields': (
            'name_fr', 'slug_fr',
            'name_ar', 'slug_ar',
            'name_es', 'slug_es',
            'name_it', 'slug_it'
        )}),
        ('Short Descriptions', {'fields': (
            'short_description_en', 'short_description_fr', 'short_description_ar',
            'short_description_es', 'short_description_it'
        )}),
        ('Long Descriptions', {'fields': (
            'description_en', 'description_fr', 'description_ar',
            'description_es', 'description_it'
        )}),
        ('Ingredients List', {'fields': (
            'ingredients_en', 'ingredients_fr', 'ingredients_ar', 'ingredients_es', 'ingredients_it'
        )}),
        ('Usage Recommendations', {'fields': (
            'usage_ideas_en', 'usage_ideas_fr', 'usage_ideas_ar', 'usage_ideas_es', 'usage_ideas_it'
        )}),
        ('Technical B2B specs', {'fields': (
            'acidity', 
            'shelf_life_en', 'shelf_life_fr', 'shelf_life_ar', 'shelf_life_es', 'shelf_life_it',
            'storage_conditions_en', 'storage_conditions_fr', 'storage_conditions_ar', 'storage_conditions_es', 'storage_conditions_it',
            'origin_en', 'origin_fr', 'origin_ar', 'origin_es', 'origin_it'
        )}),
        ('Logistics Configurations', {'fields': (
            'packaging_formats', 'certifications'
        )}),
    )


@admin.register(B2BInquiry)
class B2BInquiryAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'country', 'email', 'phone', 'requested_products', 'quantity', 'created_at')
    list_filter = ('country', 'created_at')
    search_fields = ('company_name', 'country', 'email', 'requested_products')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Company & Contact Details', {'fields': (
            'company_name', 'country', 'email', 'phone'
        )}),
        ('Inquiry Logistics Specifications', {'fields': (
            'requested_products', 'packaging_format', 'quantity'
        )}),
        ('Custom Messages', {'fields': [
            'custom_message'
        ]}),
        ('Metadata', {'fields': [
            'created_at'
        ]}),
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'author_en', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title_en', 'title_fr', 'content_en')
    prepopulated_fields = {'slug': ('title_en',)}
    
    fieldsets = (
        ('Core', {'fields': (
            'is_published', 'slug'
        )}),
        ('Title & Author', {'fields': (
            'title_en', 'author_en',
            'title_fr', 'author_fr',
            'title_ar', 'author_ar',
            'title_es', 'author_es',
            'title_it', 'author_it'
        )}),
        ('Excerpts', {'fields': (
            'excerpt_en', 'excerpt_fr', 'excerpt_ar', 'excerpt_es', 'excerpt_it'
        )}),
        ('Main Article Content', {'fields': (
            'content_en', 'content_fr', 'content_ar', 'content_es', 'content_it'
        )}),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(HeroMedia)
class HeroMediaAdmin(admin.ModelAdmin):
    list_display = ('page', 'media_type', 'image', 'video')
    list_editable = ('media_type',)
    fieldsets = (
        (None, {'fields': ('page', 'media_type')}),
        ('Media Files', {'fields': ('image', 'video')}),
    )

