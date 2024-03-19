from django.contrib import admin
from django.contrib.auth.models import Permission

from rango.models import Category, Page
class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url')
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)

# 让UserProfile模型数据通过django admin web界面可访问，导入新的UserProfile模块到本文件，如下：
from rango.models import UserProfile
# 下一行后，你可以使用admin接口来注册新模型
admin.site.register(UserProfile)
admin.site.register(Permission)
