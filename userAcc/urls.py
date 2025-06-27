from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    # path('register',views.registration_form,name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('signup',views.signup_view,name='signup'),
    path('login/',views.signin_view,name='login'),
    path('addAcount',views.Account_view,name='addAcount'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)