import re
import urllib
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

TICKER = 'CSCO'
URL_TEMPLATE = "https://feeds.finance.yahoo.com/" + \
    "rss/2.0/headline?s=%s&region=US&lang=en-US"

def get_article_urls(ticker):
    # Return list of URLs for articles about a stock
    link_pattern = re.compile(r"<link>[^<]*</link>")
    xml_url = URL_TEMPLATE % ticker
    xml_data = urllib.urlopen(xml_url).read()
    link_hits = re.findall(link_pattern, xml_data)
    return [h[6:-7] for h in link_hits]

def get_article_content(url):
    # input: url for a news article
    # output: approx. content of the article
    # Downloads HTML for an article and then
    # pulls data from paragraphs in the html
    paragraph_re = re.compile(r"<p>.*</p>")
    tag_re = re.compile(r"<[^>]*>")
    raw_html = urllib.urlopen(url).read()
    paragraphs = re.findall(paragraph_re, raw_html)
    all_text = " ".join(paragraphs)
    content = re.sub(tag_re, "", all_text)
    return content

def text_to_bag(txt):
    # Input: bunch of text
    # Output: bag-of-words of lemmas
    # Also removes stop words
    lemmatizer  = WordNetLemmatizer()
    txt_as_ascii = txt.decode(
        'ascii', 'ignore').lower()
    tokens = nltk.tokenize.word_tokenize(txt_as_ascii)
    words = [t for t in tokens if t.isalpha()] 
    lemmas = [lemmatizer.lemmatize(w) for w in words]
    stop = set(stopwords.words('english'))
    nostops = [l for l in lemmas if l not in stop]
    return nltk.FreqDist(nostops)

def count_good_bad(bag):
    # Input: bag-of-words of lemmas
    # Output: number of words that are good, bad
    good_synsets = set(wn.synsets('good') + \
        wn.synsets('up'))
    bad_synsets = set(wn.synsets('bad') + \
        wn.synsets('down'))
    n_good, n_bad = 0, 0
    for lemma, ct in bag.items():
        ss = wn.synsets(lemma)
        if good_synsets.intersection(ss): n_good += 1
        if bad_synsets.intersection(ss): n_bad += 1
    return n_good, n_bad


urls = get_article_urls(TICKER)
contents = [get_article_content(u) for u in urls]
bags = [text_to_bag(txt) for txt in contents]
counts = [count_good_bad(txt) for txt in bags]
n_good_articles = len([_ for g, b in counts if g > b])
n_bad_articles = len([_ for g, b in counts if g < b])

print "There are %i good articles and %i bad ones" % (n_good_articles, n_bad_articles)
