from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from blackD.pagamento.pagseguro import pagseguro_check_notification, pagseguro_create_invoice

INVOICE_DESCRIPTION = "Assinatura"
INVOICE_AMOUNT = "19.90"
INVOICE_SUBSCRIPTION_ITEM_ID = 1  #id do produto da assinatura

# Create your views here.
@csrf_exempt
def pagseguro_notification(request):
    notificationCode = request.POST['notificationCode']

    payed, id_user, id_produto = pagseguro_check_notification(notificationCode)

    print(payed, id_user, id_produto)

    #TODO change user as payed
    if payed and id_produto == str(INVOICE_SUBSCRIPTION_ITEM_ID):
        #usuario pagando a assinatura
        user = User.objects.get(id=id_user)
        user.email = "payed" + user.email
        user.save()
        print(user.email)

    return HttpResponse("true")



@login_required
def create_subscription_invoice(request):
    usr = request.user
    user_id = usr.id
    nome = usr.username
    email = usr.email

    print(user_id)

    item_id = INVOICE_SUBSCRIPTION_ITEM_ID
    valor = INVOICE_AMOUNT
    description = INVOICE_DESCRIPTION

    response = pagseguro_create_invoice(valor, user_id, nome + " sobrenome", email, description, item_id)

    if response != -1:
        return HttpResponse(response)
    else:
        return HttpResponse("Erro na criação da fatura de pagamento")
