#! ~/opt/anaconda3/bin/python
# -*- coding: utf-8 -*-

from tornado import options, web, httpserver, ioloop
import os.path
from index_handler import HomeHandler, DatasyncHandler

class Application(web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/dashboard/datasync", DatasyncHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            cookie_secret="027bb1b670eddf0392cdda8709268a17b58b7",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


options.parse_command_line()
http_server = httpserver.HTTPServer(Application())
http_server.listen(9999)
options.define_logging_options = "info"
ioloop.IOLoop.current().start()
