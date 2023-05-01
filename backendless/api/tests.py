from django.test import TestCase
from django.contrib.auth.models import User
from .models import Endpoint, TestArea, ApiKey

class EndpointModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_endpoint(self):
        endpoint = Endpoint.objects.create(
            user=self.user,
            name='Test Endpoint',
            url_suffix='test_endpoint',
            api_payload_format='{"input": "string"}',
            prompt='Process the input: {{input}}',
            llm_model='gpt-3',
            api_payload_injection='input',
            post_llm_processing_rules='{"output": "string"}',
            response_typing='{"output": "string"}'
        )
        self.assertEqual(endpoint.name, 'Test Endpoint')
        self.assertEqual(endpoint.user, self.user)

class TestAreaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.endpoint = Endpoint.objects.create(
            user=self.user,
            name='Test Endpoint',
            url_suffix='test_endpoint',
            api_payload_format='{"input": "string"}',
            prompt='Process the input: {{input}}',
            llm_model='gpt-3',
            api_payload_injection='input',
            post_llm_processing_rules='{"output": "string"}',
            response_typing='{"output": "string"}'
        )

    def test_create_test_area(self):
        test_area = TestArea.objects.create(
            endpoint=self.endpoint,
            test_case='{"input": "example"}'
        )
        self.assertEqual(test_area.endpoint, self.endpoint)
        self.assertEqual(test_area.test_case, '{"input": "example"}')

class ApiKeyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_api_key(self):
        api_key = ApiKey.objects.create(
            user=self.user,
            key='example_key',
            encrypted_key='encrypted_example_key',
            key_type='openai'
        )
        self.assertEqual(api_key.user, self.user)
        self.assertEqual(api_key.key, 'example_key')
        self.assertEqual(api_key.key_type, 'openai')
