#!/usr/bin/env python

__version__ = "0.1"

import re
import sys
import urlparse
from optparse import OptionParser

try:
    # cli entry points are messing with our imports (setup.py)
    import json, requests, feedparser
    from mail import helper as mail
except ImportError, e:
    pass

parser = OptionParser()

parser.add_option("-a", "--add", dest = "add", help = "add new url to monitor", default = False)
parser.add_option("-e", "--email", dest = "email", help = "add new email to send results to", default = False)
parser.add_option("-f", "--fetch", action = "store_true", dest = "fetch", help = "fetch all the stored urls", default = False)
parser.add_option("-i", "--index", action = "store_true", dest = "index_only", help = "only index, don't send emails", default = False)

opts, args = parser.parse_args()


try:
    urls = json.loads(open('urls.json').read())
except:
    urls = []

try:
    index = json.loads(open('index.json').read())
except: 
    index = []

try:
    emails = json.loads(open('emails.json').read())
except:
    emails = []


def unescape(text):
    """
    Taken from http://effbot.org/zone/re-sub.htm#unescape-html
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def _make_feed_url(url):
    parsed = urlparse.urlparse(url)
    path = '/rssfeed' + parsed.path 
    
    return 'http://www.gumtree.com%s?%s' % ( path , parsed.query )

def add(url):
    if not 'rssfeed' in url:
        url = _make_feed_url(url)
    if url not in urls:
        urls.append(url)
        open('urls.json','w').write(json.dumps(urls))

def _send_entry(entry):
    spacer = 78 * u'-'
    joiner = u'\n%s\n' % spacer

    content = joiner.join([
        unescape(c.value) for c in entry.content
        ] )

    content += joiner
    content += entry['link']

    content = content.encode('utf-8')
    title = u'[%s] %s' % (entry.updated , entry.title)
    title = title.encode('utf-8')

    message = mail.plain(content, from_name = "Gumtree Monitor", from_email = "gumtree@owns.ch", subject = title, to = emails)
    mail.send_smtp(message, 'localhost')

def fetch():
    for url in urls:
        print "*** Feed: ", url
        entries = feedparser.parse(requests.get(url).text)['entries']
        for entry in entries:
            if entry['link'] not in index:
                index.append(entry['link'])
                if not opts.index_only:
                    print "Sending ", entry.title
                    _send_entry(entry)
                else:
                    print "Indexing ", entry.title

    open('index.json', 'w').write(json.dumps(index))        


def addmail(email):
    if email not in emails:
        emails.append(email)
        open('emails.json', 'w').write(json.dumps(emails))

def main():

    if opts.add:
        return add(opts.add)

    if opts.email:
        return addmail(opts.email)

    if opts.fetch:
        return fetch()

    parser.print_help()
    sys.exit(1)

if __name__ == "__main__":
    main()