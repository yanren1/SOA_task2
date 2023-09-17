from zeep import Client

# 创建SOAP客户端
client = Client('http://localhost:8000/?wsdl')

# 调用SOAP服务的方法
result = client.service.add(5, 3)
print("Result:", result)
