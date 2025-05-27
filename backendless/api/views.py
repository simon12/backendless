from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Endpoint, TestArea, ApiKey, DrinkRound
from .serializers import EndpointSerializer, TestAreaSerializer, ApiKeySerializer, DrinkRoundSerializer
from .permissions import IsEndpointOwner, IsApiKeyOwner, IsDrinkRoundCreator, CanAccessDrinkRound
from .llm import call_llm
import json

class EndpointListCreateView(generics.ListCreateAPIView):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
    permission_classes = [IsAuthenticated, IsEndpointOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        return Endpoint.objects.filter(user=self.request.user)

class EndpointRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
    permission_classes = [IsAuthenticated, IsEndpointOwner]

class TestAreaListCreateView(generics.ListCreateAPIView):
    queryset = TestArea.objects.all()
    serializer_class = TestAreaSerializer
    permission_classes = [IsAuthenticated, IsEndpointOwner]

    def perform_create(self, serializer):
        endpoint = get_object_or_404(Endpoint, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, endpoint)
        serializer.save(endpoint=endpoint)
        
    def get_queryset(self):
        return TestArea.objects.filter(endpoint__id=self.kwargs['pk'])

class TestAreaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestArea.objects.all()
    serializer_class = TestAreaSerializer
    permission_classes = [IsAuthenticated, IsEndpointOwner]

class ApiKeyListCreateView(generics.ListCreateAPIView):
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer
    permission_classes = [IsAuthenticated, IsApiKeyOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        return ApiKey.objects.filter(user=self.request.user)

class ApiKeyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer
    permission_classes = [IsAuthenticated, IsApiKeyOwner]

# DrinkRound views
class DrinkRoundListCreateView(generics.ListCreateAPIView):
    serializer_class = DrinkRoundSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DrinkRound.objects.filter(creator=self.request.user)
    
    def perform_create(self, serializer):
        endpoint_id = self.kwargs.get('endpoint_id')
        endpoint = get_object_or_404(Endpoint, pk=endpoint_id)
        
        # Check if user owns the endpoint
        if endpoint.user != self.request.user:
            return Response(
                {"detail": "You do not have permission to share this endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(creator=self.request.user, endpoint=endpoint)

class DrinkRoundRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DrinkRound.objects.all()
    serializer_class = DrinkRoundSerializer
    permission_classes = [IsAuthenticated, IsDrinkRoundCreator]

class DrinkRoundRevokeView(APIView):
    permission_classes = [IsAuthenticated, IsDrinkRoundCreator]
    
    def post(self, request, pk):
        drink_round = get_object_or_404(DrinkRound, pk=pk)
        self.check_object_permissions(request, drink_round)
        
        drink_round.is_active = False
        drink_round.save()
        
        return Response({"detail": "Drink round revoked successfully."}, status=status.HTTP_200_OK)

class SharedEndpointView(APIView):
    permission_classes = []  # Public access
    
    def get(self, request, token):
        drink_round = get_object_or_404(DrinkRound, access_token=token)
        
        # Check if the drink round is available
        if not drink_round.is_available():
            return Response(
                {"detail": "This shared endpoint is no longer available."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Return the endpoint details (without sensitive information)
        endpoint = drink_round.endpoint
        return Response({
            "drink_round": {
                "name": drink_round.name,
                "description": drink_round.description,
                "creator": drink_round.creator.username,
                "expires_at": drink_round.expires_at,
                "usage_count": drink_round.usage_count,
                "usage_limit": drink_round.usage_limit,
            },
            "endpoint": {
                "name": endpoint.name,
                "description": "Use this endpoint by sending a POST request with your data.",
            }
        })
    
    def post(self, request, token):
        drink_round = get_object_or_404(DrinkRound, access_token=token)
        
        # Check if the drink round is available
        if not drink_round.is_available():
            return Response(
                {"detail": "This shared endpoint is no longer available."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Process the request using the endpoint
        endpoint = drink_round.endpoint
        
        try:
            # Get API key for the endpoint owner
            api_key = ApiKey.objects.filter(user=endpoint.user, key_type='Internal').first()
            if not api_key:
                return Response(
                    {"detail": "No API key available for this endpoint."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Process the request data according to the endpoint's configuration
            request_data = request.data
            
            # Call the LLM with the endpoint's configuration
            llm_response = call_llm(
                api_key=api_key.encrypted_key,
                model=endpoint.llm_model,
                prompt=endpoint.prompt,
                max_tokens=1000  # Default max tokens
            )
            
            # Increment the usage count
            drink_round.increment_usage()
            
            return Response({
                "response": llm_response,
                "remaining_uses": drink_round.usage_limit - drink_round.usage_count
            })
            
        except Exception as e:
            return Response(
                {"detail": f"Error processing request: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
