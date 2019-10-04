from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from users import views as user_views

app_name = 'apps'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('', include('tasks.urls', namespace='home')),

    # Registration and SignIn related
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_request, name="login"),
    path('logout/', user_views.logout_request, name="logout"),

    # Profile related
    path('profile/', user_views.show_profile, name="profile"),
    path('profile/edit/<int:pk>', user_views.student_update, name="edit_profile"),

    # Deactivation related
    path('deactivate/', user_views.deactivate, name="deactivate"),
    path('reactivate/', user_views.reactivate, name="reactivate"),

    # Password reset related
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(
        'reset/<str:uidb64>/<str:token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
