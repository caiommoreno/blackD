# from django.test import TestCase
# from blackD.core.forms import ProductForm, SaleForm
#
#
# class ProductFormTest(TestCase):
#     def test_has_fields(self):
#         """Form must have 4 fields."""
#         form = ProductForm()
#         expected = ['nome', 'categoria', 'preco_custo', 'preco_venda']
#         self.assertSequenceEqual(expected, list(self.form.fields))
#
#     def test_preco_is_digit(self):
#         """Preco must only accept digits"""
#         data = dict(nome='Pizza', categoria='Comida',preco_custo='dasdasd',
#                     preco_venda='321')
#         form = ProductForm(data)
#         form.is_valid()
#
#         self.assertListEqual(['preco_custo'], list(form.errors))
#
#     # # Test if html is loading by Django templates
#     # def test_html(self):
#     #     """Html must contain input tags"""
#     #     self.assertContains(self.resp, '<form')
#     #     self.assertContains(self.resp, '<input', 5)
#
#
# class SaleFormTest(TestCase):
#     def test_has_fields(self):
#         """Form must have 4 fields."""
#         form = SaleForm()
#         expected = ['nome', 'categoria', 'preco_custo', 'preco_venda']
#         self.assertSequenceEqual(expected, list(self.form.fields))
