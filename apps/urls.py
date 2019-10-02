from django.urls import include, path
from django.contrib import admin
from users import views as user_views
from django.contrib.auth import views as auth_views
app_name = 'apps'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('', include('tasks.urls', namespace='home')),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_request, name="login"),
    path('logout/', user_views.logout_request, name="logout"),
]