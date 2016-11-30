# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

env = Environment(loader = FileSystemLoader('templates'))
template = env.get_template('router_template.txt')

with open('routers_info.csv') as f:
    routers = csv.DictReader(f)

    for router in routers:
        r1_conf = router['name']+'_r1.txt'
        with open(r1_conf,'w') as f:
            f.write(template.render( router ))

