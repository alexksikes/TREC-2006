import os, re, sys, glob
from xml.dom import minidom
from fix_xml import *

def run(xml_path):
    articles = glob.glob(os.path.join(xml_path, '*'))
    nb_articles = len(articles)
    for article in articles:
        pmid = re.sub('.xml', '', article.split('/')[-1])
        parse(fix_xml(open(article, 'r').read()), pmid)
        
def parse(xml, pmid):
    try:
        xmldoc = minidom.parseString(xml)
    except Exception, e:
        sys.stderr.write("Error on file: %s: %s\n") % (pmid, e)
        return
    reflist = xmldoc.getElementsByTagName('section')
    for r in reflist:
        section = r.attributes['id'].value
        start = r.childNodes[1].attributes['start'].value
        end = r.childNodes[-2].attributes['end'].value
        print "%s\t%s\t%s\t%s" % (pmid, section, start, end)
        
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python section_spans.py xml_path"
    else:
        run(sys.argv[1])