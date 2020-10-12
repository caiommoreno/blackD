from django.test import TestCase
from blackD.core.forms import ProductForm, SaleForm


class MyTests(TestCase):
    def test_forms(self):
        form = SaleForm()
        expected = ['data', 'cliente', 'total']
        self.assertSequenceEqual(expected, list(form.fields))

# class HomeTest(TestCase):
#     def setUp(self):
#         self.response = self.client.get('/')
#
#     def test_get(self):
#         """GET / must return status code 200"""
#         self.assertEqual(200, self.response.status_code)
#
#     def test_template(self):
#         """Must use index.html"""
#         self.assertTemplateUsed(self.response, 'index.html')
#
#
# class ProductsTest(TestCase):
#     def setUp(self):
#         self.resp = self.client.get('/products/')
#
#     # Test if url is running
#     def test_get(self):
#         """GET /products/ must return status code 200"""
#         self.assertEqual(200, self.resp.status_code)
#
#     # Test if template is loading
#     def test_template(self):
#         """Must use products.html"""
#         self.assertTemplateUsed(self.resp, 'products.html')
#
#
#     # Connection between Django and html template
#     # def test_has_form(self):
#     #     """Context must have products"""
#     #     form = self.resp.context['form']
#     #     self.assertIsInstance(form, ProductForm)
#
# class AddProductsTest(TestCase):
#
#     def setUp(self):
#         self.resp = self.client.get('/add_products/')
#
#     # Test if url is running
#     def test_get(self):
#         """GET /products/ must return status code 200"""
#         self.assertEqual(200, self.resp.status_code)
#
#     # Test if template is loading
#     def test_template(self):
#         """Must use products.html"""
#         self.assertTemplateUsed(self.resp, 'add_item.html')
#
#     # Test csrf certificate
#     def test_csrf(self):
#         """Html must contain csrf"""
#         self.assertContains(self.resp, 'csrfmiddlewaretoken')
#
#
# class ProductsTest(TestCase):
#     def setUp(self):
#         self.resp = self.client.get('/products/')
#
#     # Test if url is running
#     def test_get(self):
#         """GET /products/ must return status code 200"""
#         self.assertEqual(200, self.resp.status_code)
#
#     # # Test if template is loading
#     # def test_template(self):
#     #     """Must use products.html"""
#     #     self.assertTemplateUsed(self.resp, 'products.html')
#
#
#     # Connection between Django and html template
#     # def test_has_form(self):
#     #     """Context must have products"""
#     #     form = self.resp.context['form']
#     #     self.assertIsInstance(form, ProductForm)
# #
# # class AddProductsTest(TestCase):
# #
# #     def setUp(self):
# #         self.resp = self.client.get('/add_products/')
# #
# #     # Test if url is running
# #     def test_get(self):
# #         """GET /products/ must return status code 200"""
# #         self.assertEqual(200, self.resp.status_code)
# #
# #     # Test if template is loading
# #     def test_template(self):
# #         """Must use products.html"""
# #         self.assertTemplateUsed(self.resp, 'add_item.html')
# #
# #     # Test csrf certificate
# #     def test_csrf(self):
# #         """Html must contain csrf"""
# #         self.assertContains(self.resp, 'csrfmiddlewaretoken')