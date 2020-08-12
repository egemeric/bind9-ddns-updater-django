from django.urls import path, include
from . import views
urlpatterns=[
    path('updater/<str:domain_name>/', views.get_record, name='update'),
    path('updater/<str:domain_name>/update/', views.update_record, name='update_domain'),
    path('updater/<str:domain_name>/add_domain/', views.add_domain, name='add_domain'),
    path('updater/<str:domain_name>/get_secret/',views.get_secret, name='get_secret'),
]