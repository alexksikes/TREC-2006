import os, re, sys, glob

from xml.dom import minidom

def run(xml_path):
    articles = glob.glob(os.path.join(xml_path, '*'))
    nb_articles = len(articles)
    count_a = 0
    for article in articles:
        count_a +=1
        pmid = re.sub('.xml', '', article.split('/')[-1])
        xml = open(article, 'r').read()
        xml_parsing(article, pmid)
        
def xml_parsing(xml_file, pmid):
    try:
        xmldoc = minidom.parse(xml_file)
    except Exception, e:
        print "%s\t%s" % (pmid, e)
            
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python error_check.py xml_path"
    else:
        run(sys.argv[1])