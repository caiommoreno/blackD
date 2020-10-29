import urllib.request
import json
from collections import namedtuple
from xml.etree import ElementTree
from decouple import config

DEBUG_PAYMENT = config('DEBUG_PAYMENT')

TOKEN_TEST = config('PAGSEGURO_TOKEN_TEST')
TOKEN_PRODUCTION = config('PAGSEGURO_TOKEN_PRODUCTION')

EMAIL_TEST =  config('PAGSEGURO_EMAIL_TEST')
EMAIL_PRODUCTION = config('PAGSEGURO_EMAIL_PRODUCTION')

PAGSEGURO_REQUEST_URL_TEST = 'https://ws.sandbox.pagseguro.uol.com.br/v2'
PAGSEGURO_REQUEST_URL_PRODUCTION = 'https://ws.pagseguro.uol.com.br/v2'

PAGSEGURO_CHECKOUT_SCREEN_URL_TEST = 'https://sandbox.pagseguro.uol.com.br/v2/checkout/payment.html?code='
PAGSEGURO_CHECKOUT_SCREEN_URL_PRODUCTION = 'https://pagseguro.uol.com.br/v2/checkout/payment.html?code='

TOKEN = ''
EMAIL = ''
PAGSEGURO_REQUEST_URL = ''
PAGSEGURO_CHECKOUT_SCREEN_URL = ''

PAGSEGURO_URLS = ''

if DEBUG_PAYMENT == 'True':
    TOKEN = TOKEN_TEST
    EMAIL = EMAIL_TEST
    PAGSEGURO_REQUEST_URL = PAGSEGURO_REQUEST_URL_TEST
    PAGSEGURO_CHECKOUT_SCREEN_URL = PAGSEGURO_CHECKOUT_SCREEN_URL_TEST
else:
    TOKEN = TOKEN_PRODUCTION
    EMAIL = EMAIL_PRODUCTION
    PAGSEGURO_REQUEST_URL = PAGSEGURO_REQUEST_URL_PRODUCTION
    PAGSEGURO_CHECKOUT_SCREEN_URL = PAGSEGURO_CHECKOUT_SCREEN_URL_PRODUCTION

PagseguroUrls = namedtuple('PagseguroUrls', 'ORIGINAL INVOICES NOTIFICATIONS')

PAGSEGURO_URLS = PagseguroUrls(
    ORIGINAL = PAGSEGURO_REQUEST_URL,
    INVOICES = PAGSEGURO_REQUEST_URL + '/checkout',
    NOTIFICATIONS = PAGSEGURO_REQUEST_URL + '/transactions/notifications/'
)



def url_add_parameter(url, params):
    return (url + ('&' if url.find('?') != -1 else '?') + params) if params != '' else url

def url_add_token_email(url):
    return url_add_parameter(url, 'email=' + EMAIL + '&token=' + TOKEN)
    

def pagseguro_request(url, post_data=None, method='GET'):    
    url = url_add_token_email(url)

    print(url)
    
    if method == 'GET':
        req = urllib.request.Request(url)
        try:
            res = urllib.request.urlopen(req)
        except Exception as e:
            print(e)
            return -1
    elif method == 'PUT':
        DATA = urllib.parse.urlencode(post_data).encode("utf-8")
        req = urllib.request.Request(url, data=DATA, method='PUT')
        try:
            #print(post_data)
            res = urllib.request.urlopen(req)
        except Exception as e:
            #print(post_data, e, e.fp.read())
            print(e)
            return -1    
    elif method == 'POST':
        req = urllib.request.Request(url)
        #jsondata = json.dumps(post_data)
        #jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
        #req.add_header('Content-Length', len(jsondataasbytes))
        data_bytes = post_data.encode('utf-8')
        try:
            #print(post_data)
            res = urllib.request.urlopen(req, data_bytes)        
        except Exception as e:
            print(e)
            return -1    
            
    res_body = res.read()
    #response_json = json.loads(res_body)

    return res_body



def pagseguro_create_invoice(valor, id, nome, email, description, item_id):
    '''
        @params:
            valor: string representando o valor com separador de casas decimais sendo o . (ponto)
    '''
    post_data = 'currency=BRL\
&itemId1=' + str(item_id) + '\
&itemDescription1='+ description + '\
&itemAmount1=' + valor + '\
&itemQuantity1=1\
&itemWeight1=1000\
&itemShippingCost1=0.00\
&reference=' + str(id) + '\
&senderName=' + nome + '\
&senderAreaCode=99\
&senderPhone=999999999\
&senderEmail=' + email + '\
&shippingType=3\
&shippingAddressRequired=true\
&shippingAddressStreet=Av. PagSeguro\
&shippingAddressNumber=9999\
&shippingAddressComplement=99o andar\
&shippingAddressDistrict=Jardim Internet\
&shippingAddressPostalCode=99999999\
&shippingAddressCity=Cidade Exemplo\
&shippingAddressState=SP\
&shippingAddressCountry=BRA\
&timeout=25\
&enableRecover=false'

    response = pagseguro_request(PAGSEGURO_URLS.INVOICES, post_data, 'POST')

    if response != -1:
        root = ElementTree.fromstring(response)
        try:
            for child1 in root:
                if child1.tag == 'code':
                    return PAGSEGURO_CHECKOUT_SCREEN_URL + child1.text
        except Exception as e:
            error = str(e)
            print(error)

    return -1


def pagseguro_check_notification(notification_code):
    response = pagseguro_request(PAGSEGURO_URLS.NOTIFICATIONS + notification_code)

    payed = False
    id_user = -1
    id_product = ''

    if response != -1:
        root = ElementTree.fromstring(response)
        try:
            for child1 in root:
                if child1.tag == 'reference':
                    id_user = child1.text 
                elif child1.tag == 'status':
                    if child1.text == '3':
                        payed = True
                    else:
                        payed = False
                elif child1.tag == 'items':
                    for item in child1:
                        for items_of_items in item:
                            if items_of_items.tag == 'id':
                                id_product = items_of_items.text
        except Exception as e:
            error = str(e)

    return payed, id_user, id_product


def test_create_invoice():
    return pagseguro_create_invoice('19.90', 1, "Rafael Yamada", "rafael.yamada@gmail.com", "Assinatura", 1)
