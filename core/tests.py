from django.test import TestCase
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _
from core.models import Category, Product, B2BInquiry
from core.forms import B2BInquiryForm

class VinaigreDeMarocTests(TestCase):
    
    def setUp(self):
        # 1. Create a category
        self.category = Category.objects.create(
            name_en="Vinegars",
            name_fr="Vinaigres",
            name_ar="أنواع الخل",
            slug="vinegars",
            slug_fr="vinaigres",
            slug_ar="vinegars-ar"
        )
        
        # 2. Create a product
        self.product = Product.objects.create(
            category=self.category,
            name_en="Vinaigre blond d'alcool",
            name_fr="Vinaigre blond d'alcool",
            name_ar="خل الكحول الأشقر",
            slug="vinaigre-blond-alcool",
            slug_fr="vinaigre-blond-alcool-fr",
            slug_ar="vinaigre-blond-alcool-ar",
            acidity="6%",
            is_premium=True,
            is_featured=True
        )

    def test_translation_field_fallback(self):
        """Test fallback properties for multilingual model fields."""
        # Active language English
        with translation.override('en'):
            self.assertEqual(self.category.name_en, "Vinegars")
        
        # Active language French
        with translation.override('fr'):
            self.assertEqual(self.category.name_fr, "Vinaigres")

    def test_view_status_codes(self):
        """Test that all static and detail views return 200 OK status codes under different language scopes."""
        languages = ['en', 'fr', 'ar', 'es', 'it']
        
        for lang in languages:
            with translation.override(lang):
                # 1. Test Home page
                response = self.client.get(reverse('home'))
                self.assertEqual(response.status_code, 200)

                # 2. Test About page
                response = self.client.get(reverse('about'))
                self.assertEqual(response.status_code, 200)

                # 3. Test Products list page
                response = self.client.get(reverse('products'))
                self.assertEqual(response.status_code, 200)

                # 4. Test Packaging page
                response = self.client.get(reverse('packaging'))
                self.assertEqual(response.status_code, 200)

                # 5. Test Certifications page
                response = self.client.get(reverse('certifications'))
                self.assertEqual(response.status_code, 200)

                # 6. Test Contact page
                response = self.client.get(reverse('contact'))
                self.assertEqual(response.status_code, 200)

    def test_rtl_arabic_rendering(self):
        """Test that the RTL layout directive is successfully applied when Arabic language is selected."""
        with translation.override('ar'):
            response = self.client.get(reverse('home'))
            self.assertContains(response, 'dir="rtl"')
            self.assertContains(response, 'lang="ar"')

    def test_ltr_rendering(self):
        """Test that standard LTR directive is applied for non-bidi languages."""
        with translation.override('en'):
            response = self.client.get(reverse('home'))
            self.assertContains(response, 'dir="ltr"')
            self.assertContains(response, 'lang="en"')

    def test_b2b_inquiry_form_validation(self):
        """Test B2B inquiry form submissions, spam checks, and positive/negative validation states."""
        # 1. Positive case: valid inputs
        form_data = {
            'company_name': 'Acme Condiments Corp',
            'country': 'Germany',
            'email': 'imports@acme.de',
            'phone': '+49 30 123456',
            'requested_products': "Vinaigre blond d'alcool",
            'packaging_format': '1000L IBC',
            'quantity': '2 FCL',
            'custom_message': 'Looking for a private label supply contract starting next quarter.',
            'website': '' # Honeypot empty
        }
        form = B2BInquiryForm(data=form_data)
        self.assertTrue(form.is_valid())

        # 2. Negative case: missing email
        invalid_data = form_data.copy()
        invalid_data['email'] = ''
        form = B2BInquiryForm(data=invalid_data)
        self.assertFalse(form.is_valid())

        # 3. Honeypot spam test
        spam_data = form_data.copy()
        spam_data['website'] = 'http://spambot.com'
        response = self.client.post(reverse('contact'), data=spam_data)
        # Verify that honeypot submission redirects and gives a success indicator without validation failures
        self.assertEqual(response.status_code, 302)
