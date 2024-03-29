#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Scott Burns <scott.s.burns@gmail.com>'
__license__ = 'BSD 3-Clause'


import re
import time

from redcap import Project
from ebrl.mail import mail
from ebrl.config import rc as redcap_keys

URL = 'https://redcap.vanderbilt.edu/api/'
TO = ('scott.s.burns@vanderbilt.edu','heather.c.harris@vanderbilt.edu', 'nikki.davis@vanderbilt.edu')
#TO = ('scott.s.burns@vanderbilt.edu',)

if __name__ == '__main__':

    project = Project(URL, redcap_keys['rc'])    
    
    #  Fields we want from redcap
    fields = ['scan_num', 'im_date', 'eprime_number']

    data = project.export_records(fields=fields)
    
    #  Sort on behav id
    data.sort(key=lambda x: int(x['participant_id'].split('_')[0]))

    body = """<html><body><h2>RCV Redcap database as of {time}</h2>
    
<table border="1">
<tr><th>{0}</th><th>{1}</th><th>{2}</th></tr>
{d}
</table>
<p> Total scans: {tot_scans} </p>
</body></html>
    """
    
    d = '\n'.join(["<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>".format(x['participant_id'], 
        x['scan_num'], x['im_date']) for x in data])
    
    tot_subs = len(d)
    tot_scans = len([x for x in data if re.match('(\d){4,6}', x['scan_num']) and int(x['scan_num']) > 0])
    
    body_to_send = body.format('ID', 'Scan Num', 'Scan Date', d=d,
        time=time.strftime('%A, %d %b %Y'), tot_scans=tot_scans)
    subject = "[EBRL Automated Email] Reading Comprehension Redcap (Imaging)"
    #  print body_to_send
    mail(TO, subject, body_to_send, body_type='html')
