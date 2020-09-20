from django.test import TestCase


# Create your tests here.
from blackD.core.forms import ProductForm


class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'index.html')


class ProductsTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/products/')

    # Test if url is running
    def test_get(self):
        """GET /products/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    # Test if template is loading
    def test_template(self):
        """Must use products.html"""
        self.assertTemplateUsed(self.resp, 'products.html')

    # Test if html is loading by Django templates
    # def test_html(self):
    #     """Html must contain input tags"""
    #     self.assertContains(self.resp, '<form')
    #     self.assertContains(self.resp, '<input', 4)
    #     self.assertContains(self.resp, 'type="text"', 2)
    #     self.assertContains(self.resp, 'type="number"', 2)

    # Test csrf certificate
    # def test_csrf(self):
    #     """Html must contain csrf"""
    #     self.assertContains(self.resp, 'csrfmiddlewaretoken')

    # Connection between Django and html template
    def test_has_form(self):
        """Context must have products"""
        form = self.resp.context['form']
        self.assertIsInstance(form, ProductForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['nome', 'categoria', 'preco_custo', 'preco_venda'], list(form.fields))

