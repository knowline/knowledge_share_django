from django import forms
from rango.models import Page, Category, UserProfile 
from django.contrib.auth.models import User  
from django.forms import BoundField
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="请输入目录名。")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="请输入要添加内容的标题")
    url = forms.URLField(max_length=200, help_text="请输入要添加内容的网址(URL).")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('https://'):
            url = 'https://' + url
            cleaned_data['url'] = url

            return cleaned_data

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')

# 添加以下两个类，继承了forms.modelform。第一个用于基本user类，第二个用于Userprofile类。
# 以下两个类允许HTML表单显示必要的表格字段，用于特定的模型。大大降低了工作量。
# Meta是嵌套类，描述了特定类中额外的属性。每个meta类支持一个model字段，也可以在里面定义
# 需要排除的字段，来指示哪个字段应该呈现在表单中。此处我们只想显示username,email,password.
 
class UserForm(forms.ModelForm):
# 如果用户输入密码该密码应该不能被看到。以下升级password属性，指定该charfiled实例应该隐藏用户的输入。
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('username','email','password')


#注册它的时候并不注册USER，需要建立联系在rango/views.py中register方法

class UserProfileForm(forms.ModelForm):  
    # website = forms.URLField(required=False)
    # picture = forms.ImageField(required=False)      
    class Meta:
        model = UserProfile
        fields=('website','picture')