from django.core.exceptions import ValidationError


def validate_preco(value):
    if not value.isdigit():
        raise ValidationError('PreÃ§o deve conter apenas numeros.', 'digits')
    #
    # if len(value) != 11:
    #     raise ValidationError('CPF deve ter 11 números.', 'length')