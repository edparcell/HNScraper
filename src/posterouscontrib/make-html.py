#!/usr/bin/env python

'''
Created on Sep 15, 2010

@author: ed
'''

import ConfigParser
import hnscraper
from mako.template import Template
import logging
import sys
import os

logging.basicConfig(level=logging.ERROR)
log = logging.getLogger('hn-saved')

script_path = sys.path[0]
script_name = sys.argv[0]
script_full_name = os.path.join(script_path, script_name)
log.info('Running script in %s' % script_full_name)

os.chdir(script_path)

log.info('Loading configuration')
cfg = ConfigParser.ConfigParser()
cfg.read('hn-saved.conf')
username = cfg.get('Login', 'username')
password = cfg.get('Login', 'password')
template_file = cfg.get('Template', 'file')
output_file = cfg.get('Output', 'file')

log.info('Setting up scraper')
h = hnscraper.HNScraper()
log.info('Logging into Hacker News')
h.login_with_google(username, password)
log.info('Logged into Hacker News')

c = 1
log.info('Loading saved stories page %d' % c)
h.nav_saved_stories()
stories = []
while True:
    stories.extend(h.get_current_page_stories())
    if not h.more_available():
        break
    c = c + 1
    log.info('Loading saved stories page %d' % c)
    h.nav_more()
log.info('Loading saved stories complete. Found %d stories.' % len(stories))
log.debug('stories: %s' % str(stories))

log.info('Loading mako template file')
template = Template(filename=template_file)
log.info('Rendering html output file')
output = template.render_unicode(stories=stories).encode('utf-8', 'replace')
log.info('Rendering html output file complete')

log.info('Saving html output')
f=file(output_file, 'w')
f.write(output)
f.close()
log.info('Html output saved')

log.info('Finished. Exiting.')
