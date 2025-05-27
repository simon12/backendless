"""
URL configuration for backendless project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from api.models import Endpoint, DrinkRound
from api.views import SharedEndpointView

@login_required
def dashboard(request):
    endpoints = Endpoint.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'endpoints': endpoints})

@login_required
def endpoint_detail(request, pk):
    endpoint = Endpoint.objects.get(pk=pk)
    return render(request, 'endpoint.html', {'endpoint': endpoint})

@login_required
def endpoint_create(request):
    return render(request, 'endpoint.html')

@login_required
def test_area(request, pk):
    endpoint = Endpoint.objects.get(pk=pk)
    return render(request, 'test_area.html', {'endpoint': endpoint})

@login_required
def drink_rounds(request):
    drink_rounds = DrinkRound.objects.filter(creator=request.user)
    return render(request, 'drink_rounds.html', {'drink_rounds': drink_rounds})

@login_required
def drink_round_create(request, endpoint_id):
    endpoint = Endpoint.objects.get(pk=endpoint_id)
    if endpoint.user != request.user:
        return redirect('dashboard')
    return render(request, 'drink_round_create.html', {'endpoint': endpoint})

def shared_endpoint_view(request, token):
    try:
        drink_round = DrinkRound.objects.get(access_token=token)
        if not drink_round.is_available():
            return render(request, 'error.html', {
                'error_message': 'This shared endpoint is no longer available.'
            })
        endpoint = drink_round.endpoint
        return render(request, 'shared_endpoint.html', {
            'drink_round': drink_round,
            'endpoint': endpoint
        })
    except DrinkRound.DoesNotExist:
        return render(request, 'error.html', {
            'error_message': 'Invalid or expired share link.'
        })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', login_required(TemplateView.as_view(template_name='dashboard.html')), name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('endpoint/create/', endpoint_create, name='endpoint_create'),
    path('endpoint/<int:pk>/', endpoint_detail, name='endpoint_detail'),
    path('endpoint/<int:pk>/test_area/', test_area, name='test_area'),
    path('drink-rounds/', drink_rounds, name='drink_rounds'),
    path('endpoint/<int:endpoint_id>/share/', drink_round_create, name='drink_round_create'),
    path('shared/<str:token>/', shared_endpoint_view, name='shared_endpoint'),
]
