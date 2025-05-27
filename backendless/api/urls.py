from django.urls import path
from .views import (
    EndpointListCreateView, EndpointRetrieveUpdateDestroyView,
    TestAreaListCreateView, TestAreaRetrieveUpdateDestroyView,
    ApiKeyListCreateView, ApiKeyRetrieveUpdateDestroyView,
    DrinkRoundListCreateView, DrinkRoundRetrieveUpdateDestroyView,
    DrinkRoundRevokeView, SharedEndpointView
)

app_name = 'api'

urlpatterns = [
    # Endpoint URLs
    path('endpoints/', EndpointListCreateView.as_view(), name='endpoint-list'),
    path('endpoints/<int:pk>/', EndpointRetrieveUpdateDestroyView.as_view(), name='endpoint-detail'),
    
    # Test Area URLs
    path('endpoints/<int:pk>/test-areas/', TestAreaListCreateView.as_view(), name='test-area-list'),
    path('test-areas/<int:pk>/', TestAreaRetrieveUpdateDestroyView.as_view(), name='test-area-detail'),
    
    # API Key URLs
    path('api-keys/', ApiKeyListCreateView.as_view(), name='api-key-list'),
    path('api-keys/<int:pk>/', ApiKeyRetrieveUpdateDestroyView.as_view(), name='api-key-detail'),
    
    # Drink Round URLs
    path('endpoints/<int:endpoint_id>/drink-rounds/', DrinkRoundListCreateView.as_view(), name='drink-round-create'),
    path('drink-rounds/', DrinkRoundListCreateView.as_view(), name='drink-round-list'),
    path('drink-rounds/<int:pk>/', DrinkRoundRetrieveUpdateDestroyView.as_view(), name='drink-round-detail'),
    path('drink-rounds/<int:pk>/revoke/', DrinkRoundRevokeView.as_view(), name='drink-round-revoke'),
    path('shared/<str:token>/', SharedEndpointView.as_view(), name='shared-endpoint'),
]
