from __future__ import absolute_import

import wsgiref.simple_server

import servy.server


class Parser(servy.server.Container):
    @classmethod
    def parse_details(cls, data):
        return data.get('details')


class Echo(servy.server.Container):

    parser = Parser()

    shit = 1
    pu = ''

    @classmethod
    def echo(cls, data):
        return 'echo: {}'.format(data)


@servy.server.Server
class RiverRPC(servy.server.Container):
    echo = Echo
    shit = 1

    @classmethod
    def a(cls, pu):
        return 1


def main():
    httpd = wsgiref.simple_server.make_server('', 8000, RiverRPC)
    httpd.serve_forever()

if __name__ == '__main__':
    main()
