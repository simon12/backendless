from django import forms
from .models import Endpoint

class EndpointForm(forms.ModelForm):
    class Meta:
        model = Endpoint
        fields = [
            'name',
            'url_suffix',
            'api_payload_format',
            'prompt',
            'llm_model',
            'payload_injection_method',
            'post_processing_rules',
            'response_typing',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url_suffix': forms.TextInput(attrs={'class': 'form-control'}),
            'api_payload_format': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prompt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'llm_model': forms.Select(choices=Endpoint.LLM_MODEL_CHOICES, attrs={'class': 'form-control'}),
            'payload_injection_method': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'post_processing_rules': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'response_typing': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Add any custom validation for the Endpoint form here
        return cleaned_data
