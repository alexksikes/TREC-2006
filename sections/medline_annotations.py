import DB2, sys, re, glob, os
from locate import *

conn = DB2.connect(dsn='db', uid='uid', pwd='pwd')
curs = conn.cursor()
curs.execute('SET SCHEMA db2inst1')

def run(data_path):
    articles = glob.glob(os.path.join(data_path, '*'))
    nb_articles = len(articles)
    count = 0
    for article in articles:
        print "------------------ %s/%s ------------------" % (count, nb_articles)
        pmid = article.split('/')[-1]
        article_text = open(article, 'r').read()
        print "-- %s -- " % pmid
        abstract = get_from_db2(pmid)
        if abstract:
            (span_id, span_text) = locate(abstract, article_text, pmid) 
            if span_id:
                print "%s\t%s\t%s" % (pmid, span_id, 'abstract2')
                print "-------------- db2_abstract --------------"
                print abstract
                print "-------------- span_abstract -------------"
                print span_text
                print "----------------- span_id ----------------"
                print span_id
        count +=1

def get_from_db2(pmid):
#    s = "SELECT article_title, abstract_text FROM medline_citation WHERE pmid=%s" % pmid
    q = "SELECT abstract_text FROM medline_citation WHERE pmid=%s" % pmid
    abs = None
    try:
        curs.execute(q)
        row = curs.fetchone()
        abs = row[0].getValue()
    except Exception, e:
        sys.stderr.write("DB2 error on pmid %s: %s\n" % (pmid, e))
    return abs
    
#    abs = title = None
#    try:
#        title = row[0]
#    except Exception, e:
#        pass
#    try:
#        abs = row[1].getValue()
#    except Exception, e:
#        pass
    
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python medline_annotations.py normalized_data"
    else:
        run(sys.argv[1])
    curs.close()
    conn.close()
