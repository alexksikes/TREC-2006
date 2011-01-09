import os, re, sys, glob

from xml.dom import minidom
from fix_xml import *

def run(xml_path):
    articles = glob.glob(os.path.join(xml_path, '*'))
    nb_articles = len(articles)
    count_a = 0
    for article in articles:
        count_a +=1
        pmid = re.sub('.xml', '', article.split('/')[-1])
        xml = fix_xml(open(article, 'r').read())
        xml_parsing(xml, pmid)
        
def xml_parsing(xml, pmid):
    try:
        xmldoc = minidom.parseString(xml)
    except Exception, e:
        print "%s\t%s" % (pmid, e)
            
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python error_check.py xml_path"
    else:
        run(sys.argv[1])
