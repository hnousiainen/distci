"""
Entrypoint for execute shell worker

Copyright (c) 2013 Heikki Nousiainen, F-Secure
See LICENSE for details
"""

import json
import optparse
import sys
import logging

from . import execute_shell

__appname__ = "execute shell worker"
__usage__   = "%prog -c <configuration file>"
__version__ = "1.0"
__author__  = "Heikki Nousiainen"

def main(argv):
    """ Main function """
    parser = optparse.OptionParser(description=__doc__, version=__version__)
    parser.set_usage(__usage__)
    parser.add_option("-c", dest="config_file", help="configuration filename")
    opts, _ = parser.parse_args(argv)

    if not opts.config_file:
        print "configuration file not specified"
        parser.print_help()
        return -1

    try:
        config = json.load(file(opts.config_file, 'rb'))
    except:
        print "failed to parse configuration file"
        return -1

    if config.get('log_level'):
        log_level = logging.getLevelName(config.get('log_level').upper())
        logging.basicConfig(level=log_level, format='%(asctime)s\t%(threadName)s\t%(name)s\t%(levelname)s\t%(message)s', filename=config.get('log_file'))

    worker = execute_shell.ExecuteShellWorker(config)
    return worker.start()

def main_entry():
    return main(sys.argv)

if __name__ == "__main__":
    sys.exit(main(sys.argv))

