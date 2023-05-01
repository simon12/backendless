from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('endpoints/', views.EndpointListCreateView.as_view(), name='endpoint_list_create'),
    path('endpoints/<int:pk>/', views.EndpointRetrieveUpdateDestroyView.as_view(), name='endpoint_retrieve_update_destroy'),
    path('endpoints/<int:pk>/test_area/', views.TestAreaListCreateView.as_view(), name='test_area_list_create'),
    path('test_area/<int:pk>/', views.TestAreaRetrieveUpdateDestroyView.as_view(), name='test_area_retrieve_update_destroy'),
    path('api_keys/', views.ApiKeyListCreateView.as_view(), name='api_key_list_create'),
    path('api_keys/<int:pk>/', views.ApiKeyRetrieveUpdateDestroyView.as_view(), name='api_key_retrieve_update_destroy'),
]
