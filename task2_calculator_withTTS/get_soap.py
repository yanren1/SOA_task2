from zeep import Client

# soap service address and create client
calWsdl_url = 'https://www.genivia.com/examples/calc/calc.wsdl'
calClient = Client(calWsdl_url)

n2wWsdl_url = 'https://www.dataaccess.com/webservicesserver/NumberConversion.wso?wsdl'
n2wClient = Client(n2wWsdl_url)

# create general method of soap service
def getSoapCalMethod(method_name, *args, **kwargs):

    calMethod = getattr(calClient.service, method_name)
    return str(calMethod(*args, **kwargs))

def getSoapN2wMethod(method_name, *args, **kwargs):

    n2wMethod = getattr(n2wClient.service, method_name)
    return str(n2wMethod(*args, **kwargs))


