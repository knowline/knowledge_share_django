from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from registration.backends.simple.views import RegistrationView

from rango.forms import CategoryForm, PageForm
from rango.models import UserProfile
from rango.webhose_search import run_query
def category_list(request):
	# 以下是左侧的分类的列表
	category_objects = Category.objects.all()
	paginator = Paginator(category_objects, 10)  # 每页显示10个分类
	page_number = request.GET.get('page')  # 从查询字符串获取页码
	page_obj = paginator.get_page(page_number)
	# 以下是右侧的链接的列表
	link_objects = Page.objects.all()
	paginator_link = Paginator(link_objects, 10)
	link_number = request.GET.get('link')
	link_obj = paginator_link.get_page(link_number)
	context_dict = {'page_obj': page_obj, 'link_obj': link_obj}

	return render(request, 'categories.html', context_dict)
def link_list(request):
	return render(request, 'categories.html', {'link_obj': link_obj})
def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val
def visitor_cookie_handler(request):
	# Get the number of visits to the site.
	# We use the COOKIES.get() function to obtain the visits cookie.
	# If the cookie exists, the value returned is casted to an integer.
	# If the cookie doesn't exist, then the default value of 1 is used.
	visits = int(get_server_side_cookie(request, 'visits', '1'))

	last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))

	last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")
	# last_visit_time = datetime.now()
	# If it's been more than a day since the last visit...
	if (datetime.now() - last_visit_time).seconds > 0:
		visits = visits + 1
		# update the last visit cookie now that we have updated the count
		request.session['last_visit'] = str(datetime.now())
	else:
		visits = 1
		# set the last visit cookie
		request.session['last_visit'] = last_visit_cookie
	# update/set the visits cookie
	request.session['visits'] = visits
def index(request):
	categories = Category.objects.all()
	paginator = Paginator(categories, 10)
	page_number = request.GET.get('page')
	catpage = paginator.get_page(page_number)

	request.session.set_test_cookie()
	categories_likes_list = Category.objects.order_by('-likes')[:13]
	category_list = Category.objects.annotate(page_count=Count('page')).order_by('-page_count')[:13]
	page_list = Page.objects.order_by('-views')[:13]

	visitor_cookie_handler(request)
	# 获取访问次数
	visits = request.session.get('visits', 0)
	context_dict = {'categories': category_list, 'pages': page_list, 'categories_likes': categories_likes_list,
	                'catpage': catpage, 'visits': visits}
	# print("visits:" + request.session['visits'])
	response = render(request, 'rango/index.html', context=context_dict)
	return response
def about(request):
	categories = Category.objects.all()
	paginator = Paginator(categories, 10)
	page_number = request.GET.get('page')
	catpage = paginator.get_page(page_number)
	request.session.set_test_cookie()
	categories_likes_list = Category.objects.order_by('-likes')[:13]
	category_list = Category.objects.annotate(page_count=Count('page')).order_by('-page_count')[:13]
	page_list = Page.objects.order_by('-views')[:13]
	categories = Category.objects.all()
	context_dict = {}

	context_dict['categories'] = category_list
	context_dict['pages'] = page_list
	context_dict['categories_likes'] = categories_likes_list
	context_dict['catpage'] = catpage
	context_dict['categories'] = categories
	if request.session.test_cookie_worked():
		print("TEST COOKIE WORKED!")
		request.session.delete_test_cookie()
	# To complete the exercise in chapter 4, we need to remove the following line
	# return HttpResponse("在信息时代，知道知识在哪里比知道知识是什么更重要 here is the about page. <a href='/rango/'>View index page</a>")
	# and replace it with a pointer to ther about.html template using the render method
	return render(request, 'rango/about.html', context_dict)
from django.db.models import Count
from django.core.paginator import Paginator
def show_category(request, category_name_slug):
	context_dict = {}
	categories = Category.objects.all()
	paginator = Paginator(categories, 10)
	page_number = request.GET.get('page')
	catpage = paginator.get_page(page_number)
	categories_likes_list = Category.objects.order_by('-likes')[:13]
	category_list = Category.objects.annotate(page_count=Count('page')).order_by('-page_count')[:13]
	page_list = Page.objects.order_by('-views')[:13]
	try:
		category = Category.objects.get(slug=category_name_slug)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['pages'] = None
	context_dict['query'] = category.name
	result_list = []
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
			context_dict['query'] = query
	context_dict['result_list'] = result_list
	context_dict['categories_likes'] = categories_likes_list
	context_dict['catpage'] = catpage

	return render(request, 'rango/category.html', context_dict)
def add_category(request):
	form = CategoryForm()
	# A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new category to the database.
			category = form.save(commit=True)
			print(category, category.slug)
			# Now that the category is saved
			# We could give a confirmation message
			# But instead since the most recent catergory added is on the index page
			# Then we can direct the user back to the index page.
			return index(request)
		else:
			# The supplied form contained errors - just print them to the terminal.
			print(form.errors)
	# Will handle the bad form (or form details), new form or no form supplied cases.
	# Render the form with error messages (if any).
	return render(request, 'rango/add_category.html', {'form': form})
from django.http import JsonResponse
from .models import Category
def like_category(request, category_id):
	if request.method == 'GET':
		category = get_object_or_404(Category, pk=category_id)

		category.likes += 1
		category.save()
		return JsonResponse({'likes': category.likes})
	else:
		return JsonResponse({'error': 'like_category: Invalid request'}, status=400)
from django.contrib.auth.decorators import login_required
@login_required
def add_page(request, category_name_slug):
	categories = Category.objects.all()
	paginator = Paginator(categories, 10)
	page_number = request.GET.get('page')
	catpage = paginator.get_page(page_number)
	request.session.set_test_cookie()
	categories_likes_list = Category.objects.order_by('-likes')[:13]
	category_list = Category.objects.annotate(page_count=Count('page')).order_by('-page_count')[:13]
	page_list = Page.objects.order_by('-views')[:13]
	categories = Category.objects.all()
	context_dict = {}

	if request.session.test_cookie_worked():
		print("TEST COOKIE WORKED!")
		request.session.delete_test_cookie()
	category = get_object_or_404(Category, slug=category_name_slug)
	if not request.user.is_authenticated:
		return HttpResponse("您需要登录才能添加新页面。请先登录。")
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			page = form.save(commit=False)
			page.category = category
			page.views = 1
			page.save()
			messages.success(request, "页面已成功添加！")
			return redirect('show_category', category_name_slug=category.slug)
		else:
			messages.error(request, "添加页面失败，请检查您的输入。")
	else:
		form = PageForm()
	context_dict['categories'] = category_list
	context_dict['pages'] = page_list
	context_dict['categories_likes'] = categories_likes_list
	context_dict['catpage'] = catpage
	context_dict['categories'] = categories
	context = {'form': form, 'category': category}

	return render(request, 'rango/add_page.html', context)
def search(request):
	context_dict = {}
	# 获取所有categories并进行分页处理
	categories = Category.objects.all()
	paginator = Paginator(categories, 10)
	page_number = request.GET.get('page')
	catpage = paginator.get_page(page_number)

	# 获取按喜欢数排序的categories和按页面浏览量排序的pages
	categories_likes_list = Category.objects.order_by('-likes')[:13]
	category_list = Category.objects.annotate(page_count=Count('page')).order_by('-page_count')[:13]
	page_list = Page.objects.order_by('-views')[:13]
	context_dict['categories'] = category_list
	context_dict['pages'] = page_list
	context_dict['categories_likes'] = categories_likes_list
	context_dict['catpage'] = catpage
	result_list = []
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			# Run our Webhose function to get the results list!
			result_list = run_query(query)
			context_dict['result_list'] = result_list
	# return render(request, 'rango/search.html', {'result_list': result_list}, )
	return render(request, 'rango/search.html', context_dict)
from django.contrib import messages  # 导入messages框架
def register(request):
	if request.method == 'POST':  # 如果是HTTP POST请求
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)  # 对密码进行加密保存
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user  # 关联UserProfile与User
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()

			messages.success(request, f'账号 {user.username} 创建成功！请登录。')  # 使用messages显示成功消息
			return redirect('login_url')  # 成功后重定向到登录页，注意替换'login_url'为实际的登录页面URL名称
		else:
			# 如果表单验证失败，通过messages显示错误信息
			messages.error(request, '注册失败，请检查表单信息。')
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request,
	              'registration/registration_form.html',
	              {'user_form': user_form,
	               'profile_form': profile_form,
	               'registered': 'registered' in locals()  # 通过locals检查registered是否已定义
	               })
from django.shortcuts import render
from .forms import UserForm, UserProfileForm
def registration_complete(request):
	# return render(request, 'registration/registration_complete.html')
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')  # 获取密码字段

			# 在这里可以对用户名和密码进行进一步处理，比如保存到数据库
			return render(request, 'registration/registration_complete.html',
			              {'username': username, 'password': password})
	else:
		form = UserCreationForm()
	return render(request, 'registration/registration_form.html', {'form': form})
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from .models import Page
def track_url(request):
	page_id = request.GET.get('page_id')  # 使用 .get() 方法简化
	if page_id:
		page = get_object_or_404(Page, id=page_id)  # 简化错误处理
		page.views += 1
		page.save()
		return redirect(page.url)
	else:
		# 可以选择记录这个事件或给用户返回一个错误消息
		return HttpResponse("没有提供这个页面", status=400)
@login_required
def register_profile(request):
	form = UserProfileForm()
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES)
		if form.is_valid():
			user_profile = form.save(commit=False)
			user_profile.user = request.user
			user_profile.save()

			return redirect('index')
		else:
			print(form.errors)

	context_dict = {'form': form}

	return render(request, 'rango/profile_registration.html', context_dict)
class RangoRegistrationView(RegistrationView):
	def get_success_url(self, user):
		return reverse('register_profile')
@login_required
def profile(request, username):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return redirect('index')

	userprofile = UserProfile.objects.get_or_create(user=user)[0]
	form = UserProfileForm({'website': userprofile.website, 'picture': userprofile.picture})

	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
		if form.is_valid():
			form.save(commit=True)
			return redirect('profile', user.username)
		else:
			print(form.errors)

	return render(request, 'rango/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})
@login_required
def list_profiles(request):
	#    user_list = User.objects.all()
	userprofile_list = UserProfile.objects.all()
	return render(request, 'rango/list_profiles.html', {'userprofile_list': userprofile_list})
def user_login(request):
	# Like before, obtain the context for the user's request.
	# context = RequestContext(request)
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		username = request.POST['username']
		password = request.POST['password']

		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)

		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user:
			# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				login(request, user)
				request.session['user_name'] = username  # 在session中保存用户名
				request.session['user_password'] = password  # 在session中保存用户名
				return HttpResponseRedirect(reverse('index'))
			# return HttpResponseRedirect('/rango/')
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your Rango account is disabled.")
		else:
			# Bad login details were provided. So we can't log the user in.
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'registration/login.html')
# return render_to_response('rango/login.html', {}, context)


@login_required
def restricted(request):
	return HttpResponse("因为你登录了，你可以看到这段话！")
from django.contrib.auth import logout
# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)

	# Take the user back to the homepage.
	return HttpResponseRedirect(reverse('index'))
def registration_fail(request):
	return render(request, 'registration/registration_fail.html')
