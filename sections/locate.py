import sys, re
from text_similarity import *

p = re.compile('@#@#@ - (\d*) - @#@#@')
def locate(txt, article, pmid):
    # messed up files
    if len(article) < 400:
        sys.stderr.write("The file is too small %s\n" % pmid)
        return (None, None)
    res = p.split(article)
    i = most_similar2(txt, res)
    try:
        span_id = res[i-1]
    except Exception, e:
        sys.stderr.write("Could not get span_id for %s\n" % pmid)
        return (None, None)
    return (span_id, res[i])
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python locate.py text normalized_article"
    else:
        r = locate(sys.argv[1], open(article, 'r').read())
        if r:
            print r[1]
            print 
            print r[0]
