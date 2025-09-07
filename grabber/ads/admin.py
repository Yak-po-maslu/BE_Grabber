from django.contrib import admin
from ads.models import Ad, UploadedImageV1
from .models import FAQ, Category, SubCategory, Attribute, AttributeOption, AdAttributeValue
from ads.models import ProductComment


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'status', 'user', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'description', 'category']


@admin.register(UploadedImageV1)
class UploadedImageAdmin(admin.ModelAdmin):
    model = UploadedImageV1
    list_display = ['id', 'image', 'uploaded_at']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['question', 'answer']


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'user_name', 'rating', 'short_comment', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user_name', 'comment_text', 'product_id')
    ordering = ('-created_at',)

    def short_comment(self, obj):
        return (obj.comment_text[:50] + '...') if len(obj.comment_text) > 50 else obj.comment_text
    short_comment.short_description = 'Коментар'


class AttributeOptionInline(admin.TabularInline):
    model = AttributeOption
    extra = 1


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "category", "type", "is_filterable", "sort_order")
    list_filter = ("category", "type", "is_filterable")
    search_fields = ("name", "slug")
    inlines = [AttributeOptionInline]


@admin.register(AdAttributeValue)
class AdAttributeValueAdmin(admin.ModelAdmin):
    list_display = ("ad", "attribute", "value_text", "value_number", "value_bool", "option")
    list_filter = ("attribute",)
    search_fields = ("ad__title", "attribute__name", "value_text")


# інші моделі без дублювання Ad
admin.site.register(Category)
admin.site.register(SubCategory)
