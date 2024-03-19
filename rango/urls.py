# from django.conf.urls import url
from django.urls import path, re_path

from rango import views, views_ajax
urlpatterns = [
	re_path(r'^$', views.index, name='index'),
	re_path(r'about/$', views.about, name='about'),
	re_path(r'^add_category/$', views.add_category, name='add_category'),
	path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
	path('category/<category_name_slug>/add_page/', views.add_page, name='add_page'),
	path('categories/', views.category_list, name='category_list'),
	# path('like_category/', views.like_category, name='like_category'),
	# path('like/', views_ajax.like_category, name='ajax_like_category'),
	path('like/<int:category_id>/', views.like_category, name='like_category'),
	re_path(r'^suggest/$', views_ajax.suggest_category, name='suggest_category'),
	re_path(r'^add/$', views_ajax.auto_add_page, name='auto_add_page'),
	# 新加注册页面
	re_path(r'^register/$', views.register, name='register'),
	re_path(r'^register_profile/$', views.register_profile, name='register_profile'),
	# re_path(r'^registration_complete/$',views.register,name='registration_complete'),
	path('registration_complete/', views.registration_complete, name='registration_complete'),
	path('registration_fail/', views.registration_fail, name='registration_fail'),
	# 登录
	path('login/', views.user_login, name='login'),
	re_path(r'^logout/$', views.user_logout, name='logout'),
	# path('login/', LoginView.as_view(), name='login'),
	# path('login/', LoginView.as_view(template_name='your_template_name_here.html'), name='login'),
	# 搜索
	# re_path(r'search/$', views.search, name='search'),
	path('goto/', views.track_url, name='goto'),
	path('search/', views.search, name='search'),
	re_path(r'^restricted/', views.restricted, name='restricted'),
	re_path(r'^rango/(?P<register>[\w\-]+)/$', views.register, name='register'),
	re_path(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
	re_path(r'^profiles/$', views.list_profiles, name='list_profiles'),
]
