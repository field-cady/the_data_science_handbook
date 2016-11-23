from HTMLParser import HTMLParser
import urllib

TOPIC = "Dangiwa_Umar"
url = "https://en.wikipedia.org/wiki/%s" % TOPIC
class LinkCountingParser(HTMLParser):
    in_paragraph = False
    link_count = 0
    def handle_starttag(self, tag, attrs):
        if tag=='p': self.in_paragraph = True
        elif tag=='a' and self.in_paragraph:
            self.link_count += 1
    def handle_endtag(self, tag):
        if tag=='p': self.in_paragraph = False

html = urllib.urlopen(url).read()
parser = LinkCountingParser()
parser.feed(html)
print "there were",  parser.link_count, \
    "links in the article"
