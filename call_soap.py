from zeep import Client


# create client
client = Client('http://localhost:8000/?wsdl')



# call soap service
result = client.service.add(5, 3)
print("Result:", result)
