#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Scott Burns <scott.s.burns@gmail.com>'
__license__ = 'BSD 3-Clause'


import re
import time

from redcap import Project
from ebrl.mail import mail
from ebrl.config import rc as redcap_keys

DEBUG = False


URL = 'https://redcap.vanderbilt.edu/api/'
if DEBUG:
    TO = ('scott.s.burns@vanderbilt.edu',)
else:
    TO = ('scott.s.burns@vanderbilt.edu','heather.c.harris@vanderbilt.edu', 'nikki.davis@vanderbilt.edu')

if __name__ == '__main__':

    project = Project(URL, redcap_keys['nf'])    
    
    #  Fields we want from redcap
    fields = ['subjcateg','subjscanid', 'subjscanidv1', 'subjscanidv2', 'subjdoeday1', 'subjdoeday3']

    data = project.export_records(fields=fields)
    
    #  Sort on behav id
    data.sort(key=lambda x: int(x['studyid'].replace('B','')))

    body = """<html><body><h2>NF Redcap database as of {time}</h2>
    
<table border="1">
<tr>
<th>{0}</th>
<th>{1}</th>
<th>{2}</th>
<th>{3}</th>
<th>{4}</th>
<th>{5}</th>
<th>{6}</th>
</tr>
{d}
</table>
<p><strong>Numbers by category:</strong></p>
<p>Total: {tot}<p>
<p>{cat_info}</p>
<p><strong>Scan stats:</strong></p>
Pre: {pre_n}<br />
Post: {post_n}<br />
</body></html>"""

    cat_map = {'1':'NF', '2':'NF-RD', '3':'CNT', '4': 'RD', '5':'RD-WL', '6': 'Ineligible', '8':'Incomplete'}
    
    d = '\n'.join(["<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td><td>{6}</td></tr>".format(x['studyid'], 
        cat_map[x['subjcateg']], x['subjscanid'], x['subjscanidv1'], x['subjdoeday1'], x['subjscanidv2'], x['subjdoeday3']) for x in data])
    
    
    cat_set = set([sub['subjcateg'] for sub in data])
    
    cat_info = '\n'.join(['%s : %d<br />' % (cat_map[cat], len(filter(lambda x: x['subjcateg'] == cat, data))) for cat in cat_set])
    
    pre_n = len([x for x in data if x['subjscanidv1'] not in ('', 'NA')])
    post_n = len([x for x in data if x['subjscanidv2'] not in ('', 'NA')])
    
    tot = len(data)
    
    body_to_send = body.format('StudyID', 'Category', 'ScanID', 'Visit1 ID', 'Visit1 Date', 'Visit2 ID', 'Visit2 Date',
            d=d,time=time.strftime('%A, %d %b %Y'), cat_info=cat_info, pre_n=pre_n, post_n=post_n, tot=tot)
    subject = "[EBRL Automated Email] NF-RO1 Redcap (Imaging)"
    #  print body_to_send
    if not DEBUG:
        mail(TO, subject, body_to_send, body_type='html')
    else:
        print body_to_send