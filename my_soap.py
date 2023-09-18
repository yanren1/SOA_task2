from spyne import Application, rpc, ServiceBase, Iterable, Integer, Float
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class MyService(ServiceBase):
    @rpc(Float, Float, _returns=Iterable(Float))
    def add(self, a, b):
        yield a + b

    def sub(self, a, b):
        yield a - b

app = Application([MyService],
                  tns='my_namespace',
                  in_protocol=Soap11(validator='lxml'),
                  out_protocol=Soap11())

wsgi_application = WsgiApplication(app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8000, wsgi_application)
    print("SOAP service listening on http://0.0.0.0:8000")
    server.serve_forever()
