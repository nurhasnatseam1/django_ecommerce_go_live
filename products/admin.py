from django.contrib import admin

# Register your models here.
from .models import Product ,ProductFile


#nesting one model andmin inside another 
#the reason why it can work like that cause the the one to many relationship
#many to many would have worked as well
class ProductFileInline(admin.TabularInline):
      model=ProductFile
      extra=1

class ProductAdmin(admin.ModelAdmin):
      list_display=['__str__','slug']
      inlines=[ProductFileInline]
      class Meta:
            model=Product


admin.site.register(Product,ProductAdmin)

