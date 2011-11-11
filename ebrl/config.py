#!/usr/bin/env python
# -*- coding: utf-8 -*-
__license__ = 'BSD 3-Clause'

import os
import sys
from ConfigParser import ConfigParser

platform = os.uname()[0]
if platform == 'Linux':
    cfg_file = '/fs0/.ebrl.cfg'
else:
    cfg_file = os.path.join(os.path.expanduser('~'), '.ebrl.cfg')

cfg = ConfigParser()
cfg.read(cfg_File)

def tl2dict(tl):
    """ Takes a list of 2-tuples and returns a dict """
    data = {}
    for k,v in tl:
        data[k] = v
    return data
    
rc = tl2dict(cfg.items('rc'))
mail = tl2dict(cfg.items('email'))