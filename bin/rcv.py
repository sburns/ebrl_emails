#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Scott Burns <scott.s.burns@gmail.com>'
__license__ = 'BSD 3-Clause'

import time

from redcap import Project
from ebrl.mail import mail
from ebrl.config import rc as redcap_keys

URL = 'https://redcap.vanderbilt.edu/api/'
TO = ('scott.s.burns@vanderbilt.edu', 'nikki.davis@vanderbilt.edu')

if __name__ == '__main__':

    project = Project(URL, redcap_keys['rc'])    
    
    #  Fields we want from redcap
    fields = ['scan_num', 'im_date', 'eprime_number']

    data = project.export_records(fields=fields)
    
    #  Sort on behav id
    data.sort(key=lambda x: int(x['participant_id'].split('_')[0]))

    body = """RCV Redcap database as of {time}
    

{0:15s}{1:15s}{2:15s}
{d}
    """
    
    d = '\n'.join(["{0:15s}{1:15s}{2:15s}".format(x['participant_id'], 
        x['scan_num'], x['im_date']) for x in data])
    
    body_to_send = body.format('ID', 'Scan Num', 'Scan Date', d=d, time=time.strftime('%A, %d %b %Y'))
    subject = "[EBRL Automated Email] Reading Comprehension Redcap (Imaging)"
    mail(TO, subject, body_to_send)
