from django.contrib import admin
from .models import Product,Category,Client,Order,Clientavatar
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category','price','available')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name')
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','city','show_interested')
    def show_interested(self,obj):
        return [bt.name for bt in obj.interested_in.all()]
    filter_horizontal = ('interested_in',)
# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Client,ClientAdmin)
admin.site.register(Order)
admin.site.register(Clientavatar)