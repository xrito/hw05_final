from django.test import Client, TestCase


class AboutURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_about_url_exists_at_desired_location(self):
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_tech_url_exists_at_desired_location(self):
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)
