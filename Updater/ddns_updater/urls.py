from django.urls import path, include
from . import views
urlpatterns=[
    path('updater/<str:domain_name>/', views.get_record, name='update'),
    path('updater/<str:domain_name>/update/', views.update_record, name='update_domain'),
    path('updater/add_domain', views.update_record, name='add_domain'),
]