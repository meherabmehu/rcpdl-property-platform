from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from website.data import PROJECTS

class PublicTests(TestCase):
    def test_public_pages_render_and_project_facts_match(self):
        for route in ('/', '/projects/', '/projects/1/', '/projects/2/', '/gallery/', '/virtual-site-visit/', '/assistant/', '/inquiry/', '/about/', '/contact/', '/privacy/', '/terms/'):
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, 'href="#"')
        for project in PROJECTS:
            response = self.client.get(f'/projects/{project["id"]}/')
            self.assertContains(response, project['price'])
            self.assertContains(response, project['sqft'])

    def test_inquiry_validation_failure_retry_and_masking(self):
        url = '/api/demo/inquiry/'
        self.assertEqual(self.client.post(url, {'phone':'123','project':'1'}).status_code,422)
        self.assertEqual(self.client.post(url, {'phone':'01700000123','project':'9'}).status_code,422)
        data = {'phone':'01700000123','project':'2','name':'Example','permission':''}
        with override_settings(DEBUG=True):
            response = self.client.post(url,{**data,'scenario':'failure'})
            self.assertEqual(response.status_code,503)
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['project'],'Project 02')
        self.assertEqual(response.json()['phone'],'01XXX XXX123')
        self.assertNotIn('01700000123',response.content.decode())

    def test_csrf_is_required(self):
        self.assertEqual(Client(enforce_csrf_checks=True).post('/api/demo/inquiry/',{'phone':'01700000123','project':'1'}).status_code,403)

    def test_bangla_digits_and_optional_fields(self):
        response = self.client.post('/api/demo/inquiry/',{'phone':'০১৭০০০০০১২৩','project':'1'})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['phone'],'01XXX XXX123')

    def test_local_assistant_uses_fixture_and_unavailable_is_explicit(self):
        response = self.client.post('/api/demo/assistant/',{'message':"What is Project 02's area?"})
        self.assertContains(response,'75,00,000')
        self.assertContains(response,'3,600')
        with override_settings(DEBUG=True):
            self.assertEqual(self.client.post('/api/demo/assistant/',{'scenario':'ai-unavailable'}).status_code,503)
        with override_settings(DEBUG=False):
            self.assertEqual(self.client.post('/api/demo/assistant/',{'scenario':'ai-unavailable'}).status_code,200)

    def test_language_preserves_current_project(self):
        response = self.client.post('/i18n/setlang/',{'language':'bn','next':'/projects/2/?mode=panorama'})
        self.assertRedirects(response,'/projects/2/?mode=panorama')
        self.assertContains(self.client.get('/projects/2/'),'প্রকল্প 02')

class StaffTests(TestCase):
    @override_settings(STAFF_AUTH_AVAILABLE=False)
    def test_hosted_staff_sign_in_explains_missing_database(self):
        response = self.client.post('/staff/sign-in/', {'username':'example','password':'example'})
        self.assertEqual(response.status_code,503)
        self.assertContains(response,'persistent database',status_code=503)

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test-staff',password='test-only-password',is_staff=True)

    def test_staff_pages_need_authenticated_staff_and_demo_checkpoint(self):
        self.assertRedirects(self.client.get('/staff/'),'/staff/sign-in/')
        self.client.force_login(self.user)
        self.assertEqual(self.client.get('/staff/').status_code,403)
        with override_settings(DEBUG=True):
            self.assertEqual(self.client.post('/staff/mfa/',{'code':'000000'}).status_code,200)
            self.assertRedirects(self.client.post('/staff/mfa/',{'code':'123456'}),'/staff/')
        for route in ('/staff/','/staff/projects/1/edit/','/staff/projects/2/edit/','/staff/projects/add/','/staff/projects/1/review/','/staff/inquiries/','/staff/inquiries/1/','/staff/faqs/','/staff/contacts/'):
            self.assertEqual(self.client.get(route).status_code,200,route)

    def test_non_staff_is_restricted(self):
        self.user.is_staff = False; self.user.save()
        self.client.force_login(self.user)
        self.assertEqual(self.client.get('/staff/').status_code,403)

    def test_authentication_and_recovery_demo(self):
        self.assertEqual(self.client.post('/staff/sign-in/',{'username':'test-staff','password':'wrong'}).status_code,200)
        self.assertRedirects(self.client.post('/staff/sign-in/',{'username':'test-staff','password':'test-only-password'}),'/staff/mfa/')
        with override_settings(DEBUG=True):
            self.assertRedirects(self.client.post('/staff/mfa/?recovery=1',{'code':'DEMO-RECOVERY'}),'/staff/')
        self.assertContains(self.client.post('/staff/forgot-password/',{'email':'test@example.invalid'}),'No email has been sent')
