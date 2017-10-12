#!/usr/bin/env python

import logging
import sys

def get_logger(stream=sys.stdout, level=logging.INFO):
    log = logging.getLogger(__name__)
    sh = logging.StreamHandler(stream=stream)
    fmt = logging.Formatter(u"%(asctime)s = %(levelname)s = %(message)s")
    sh.setFormatter(fmt)
    log.addHandler(sh)
    log.setLevel(level)
    return log
