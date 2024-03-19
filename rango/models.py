from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)
	def page_count(self):
		return self.page_set.count()
	class Meta:
		verbose_name_plural = 'categories'
	def __str__(self):
		return self.name
class Page(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	def __str__(self):
		return self.title
# 因为使用了一对一关系，所以需要引用默认的用户模型。下面可以进行引用USER模型
from django.contrib.auth.models import User
# 这是一个表，表名为rango_userprofile,它与auth_user表是1:1关系。
class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# The additional attributes we wish to include.可以为空
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	# ImageField有上传属性。
	# 上传连接到MEDIA_ROOT设置：<workspace>/knowledge_share_project/media/
	# profile_image的upload_to属性使所有肖像图片上传到:<workspace>/knowledge_share_project/media/profile_images/
	# Override the __unicode__() method to return out something meaningful!
	# 记住：如果你使用python 2.7.x，还需要定义_unicode_方法，用来返回用户名的unicode变量。
	# 当该实例被请求时，返回有意义的unicode值
	def __str__(self):
		return self.user.username
	# 关于继承和扩展？
	# 有可能通过继承用户模型来增加额外的字段有吸引力。然而，因为其他应用程序可能同样想要
	# 访问用户模型，不推荐使用继承，而取之使用一个一对一关系 到你的数据库中。
	# 携带一个PIL
	# django ImageField字段使用PIL(python imaging library).如果你还没有需要用pip命令安装。
	# pip install pillow.
	# 如果没有打开jpeg支持，也可使用以下命令安装PIL:
	# pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
	# 使用pip list命令检查安装在虚拟环境、真实环境中的包。
