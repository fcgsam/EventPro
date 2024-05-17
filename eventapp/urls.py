from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

urlpatterns = [
    path('',desboard_page,name='home'),
    path('Event-page',Event_page,name='Event-page'),
    path('Task-page',Task_page,name='Task-page'),
    path('Event_user',User_Event_page,name='Event_user'),
    path('delete_user_event/',delete_user_event,name='delete_user_event'),
    path('account_page',Acount_new_page,name='account_page'),
    path('account_edit/<str:encoded_userId>/',Account_edit,name='account_edit'),
    path('edit_staff/<str:encoded_userId>/',Edit_account_admin,name='edit_staff'),
    path('profile_edit_page',profile_edit_page,name='profile_edit_page'),
    path('password_page',password_page,name='password_page'),
    path('password_reset',password_reset,name='password_reset'),
    path('profile_edit',profile_edit,name='profile_edit'),
    path('create_event',create_event,name='create_event'),
    path('update_event',get_event_data,name='update_event'),
    path('delete_event/',delete_event,name='delete_event'),
    path('new_task/',new_task,name='new_task'),
    path('login_page',login_page,name='login_page'),
    path('register_page',register_page,name='register_page'),
    path('user_info',userInfoToAssign,name='user_info'),
    path('task_table/',task_table,name='task_table'),
    path('top_task/',top_task,name='top_task'),
    path('edit_task/',edit_task_data,name='edit_task'),
    path('delete_task/',delete_task,name='delete_task'),
    path('update_status/',update_event,name='update_status'),
    path('total_amount/',total_amount,name='total_amount'),
    path('deshboard_data/',deshborad_data,name='deshboard_data'),
    path('attend_event/',attend_event,name='attend_event'),
    path('search_product',search_product,name='search_product'),
    path('new_group',new_group,name='new_group'),
    path('make_group',make_group,name='make_group'),
    path('group_info/', group_info, name='group_info'),
    path('delete_group/', delete_group, name='delete_group'),
    path('edit_group/', edit_group, name='edit_group'),
    path('get_data', get_data, name='get_data'),
    # path('<path:path>/', custom_404_view),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)