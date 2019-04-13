#!/usr/bin/python
# vim: set fileencoding=utf-8 :
# pylint: disable=E0401

"""
Geo coding proxy server
====
    $Id$  # nopep8
    $DateTime$ 04/12/2019
    $Author$ Sharad Bhadouria
    $Change$ 1
    $Reference$ https://wiki.python.org
"""

from BaseHTTPServer import HTTPServer
import time
from geo_coding_service import GeoCodingServiceDriver
import config


def main():
    """
    Main method to start the server
    :return:
    """
    server_class = HTTPServer
    httpd = server_class(('', config.PORT), GeoCodingServiceDriver)
    print(time.asctime(), "Server Starts - %s:%s" % (config.HOST, config.PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (config.HOST, config.PORT))


if __name__ == '__main__':
    main()
