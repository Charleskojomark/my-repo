from django.conf.urls import handler404, handler500
from django.urls import path 
from . import views
app_name='ojm_core'
urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('user-dashboard',views.user_dashboard,name="user_dashboard"),
    path('prof-dashboard',views.prof_dashboard,name="prof_dashboard"),
    path('all',views.all_users,name="all"),
    path('single/<int:pk>',views.single_user,name="single"),
    
    path('search',views.search_view,name="search"),
    path('categories', views.categories,name="categories"),
    path('services', views.services,name="services"),
    path('service-detail', views.service_detail,name="service_detail"),
    
    path('post-request', views.post_request, name="post_request"),
    path('user-post', views.user_post, name="user_post"),
    path('post-job', views.post_job, name="post_job"),
    path('requests', views.all_requests, name="requests"),
    path('request/<int:request_id>/', views.request_detail, name='request_detail'),
    path('request/<int:request_id>/send-quote/', views.send_quote, name='send_quote'),
    path('customer-info/<int:request_id>/',views.customer_info,name="customer_info"),
    path('notifications/', views.get_notifications, name='notifications'),
]

handler404 = 'ojm_core.views.custom_404'
handler500 = 'ojm_core.views.custom_500'



