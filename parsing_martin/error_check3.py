import os, re, sys, glob
from strip_html import *

threshold = 0.5

def run(xml_path, html_path):
    articles = glob.glob(os.path.join(xml_path, '*'))
    nb_articles = len(articles)
    count_a = 0
    for article in articles:
        count_a +=1
        pmid = re.sub('.xml', '', article.split('/')[-1])
        xml = open(article, 'r').read()
        html = open(os.path.join(html_path, pmid+'.html')).read()
        size_ratio(xml, html, pmid)

def size_ratio(xml, html, pmid):
    try:
        ratio = 1.0 * len(strip_html(xml)) / len(strip_html(html))
        if ratio < threshold:
            print "%s\t%s" % (pmid, ratio)
    except Exception, e:
        print "%s\t%s" % (pmid, -1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: python error_check.py xml_path html_path"
    else:
        run(sys.argv[1], sys.argv[2])