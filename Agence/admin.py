from django.contrib import admin
from Agence.models import Suite, Category, Order, Cart
# Register your models here.

class SuiteAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("city", "price",)
    list_display = ("city", "available", "name", "price",)

admin.site.register(Category)
admin.site.register(Suite, SuiteAdmin)
admin.site.register(Order)
admin.site.register(Cart)








 