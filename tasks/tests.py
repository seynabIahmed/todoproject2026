from django.test import SimpleTestCase
from django.urls import reverse


class HomeRedirectTests(SimpleTestCase):
    def test_home_redirects_to_admin(self):
        response = self.client.get('/')

        self.assertRedirects(
            response,
            reverse('admin:index'),
            fetch_redirect_response=False,
        )
