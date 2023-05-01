from django.shortcuts import render
from rest_framework import generics
from .models import Endpoint, TestArea, ApiKey
from .serializers import EndpointSerializer, TestAreaSerializer, ApiKeySerializer
from .permissions import IsEndpointOwner, IsApiKeyOwner

class EndpointListCreateView(generics.ListCreateAPIView):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
    permission_classes = [IsEndpointOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EndpointRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
    permission_classes = [IsEndpointOwner]

class TestAreaListCreateView(generics.ListCreateAPIView):
    queryset = TestArea.objects.all()
    serializer_class = TestAreaSerializer
    permission_classes = [IsEndpointOwner]

    def perform_create(self, serializer):
        serializer.save(endpoint=Endpoint.objects.get(pk=self.kwargs['pk']))

class TestAreaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestArea.objects.all()
    serializer_class = TestAreaSerializer
    permission_classes = [IsEndpointOwner]

class ApiKeyListCreateView(generics.ListCreateAPIView):
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer
    permission_classes = [IsApiKeyOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ApiKeyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer
    permission_classes = [IsApiKeyOwner]
