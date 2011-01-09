import sys, os, zipfile, re
from compute_spans import *
from strip_html import *
            
def run(out_folder, journals):
    nb_journals = len(journals)
    count_j = 0
    start_span_id = 0
    span_file = open(os.path.join(out_folder, 'spans_id.txt'), 'w')
    for journal in journals:
        count_j +=1
        print "=================== %s/%s ===================" % (count_j, nb_journals)
        journal_name = re.sub('.zip', '', os.path.split(journal)[1])
        print journal_name
        z = zipfile.ZipFile(journal, "r")
        articles = z.namelist()
        nb_articles = len(articles)
        count_a = 0
        for article in articles:
            count_a +=1
            print "------------------ %s | %s/%s ------------------" % (count_j, count_a, nb_articles)
            pmid = re.sub('.html|.htm', '', article.split('/')[-1])
            print pmid
            html = z.read(article)
            spans = compute_spans(start_span_id, pmid, html)
            article_file = open(os.path.join(out_folder, pmid), 'w')
            write_spans(spans, span_file, article_file, strip_html)
            article_file.close()
            start_span_id = spans[-1][0] + 1
        z.close()
    span_file.close()
                
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python normalize.py out_folder zipfiles"
    else:
        run(sys.argv[1], sys.argv[2:])