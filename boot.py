#! ~/opt/anaconda3/bin/python
# -*- coding: utf-8 -*-

import os.path
from tornado import options, web, httpserver, ioloop
from handler import HomeConfig, LotteryStop, LotterySetting, Reset

class Application(web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeConfig),
            (r"/stop", LotteryStop),
            (r"/setting", LotterySetting),
            (r"/reset", Reset)
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
http_server.listen(8888)
options.define_logging_options = "info"
ioloop.IOLoop.current().start()
