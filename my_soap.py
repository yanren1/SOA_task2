from spyne import Application, rpc, ServiceBase, Iterable, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

# 创建一个继承自ServiceBase的SOAP服务类
class MyService(ServiceBase):
    @rpc(Integer, Integer, _returns=Iterable(Integer))
    def add(self, a, b):
        yield a + b

    def sub(self, a, b):
        yield a - b


# 创建一个应用程序，将服务绑定到SOAP协议
app = Application([MyService],
                  tns='my_namespace',
                  in_protocol=Soap11(validator='lxml'),
                  out_protocol=Soap11())

# 创建WSGI应用程序
wsgi_application = WsgiApplication(app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8000, wsgi_application)
    print("SOAP service listening on http://0.0.0.0:8000")
    server.serve_forever()
