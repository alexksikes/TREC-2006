# for now field names are hard coded
field_names = ['section', 'gene', 'mesh_id']        

import os, re, sys, glob
from PyLucene import IndexWriter, StandardAnalyzer, Document, Field

a_dicts = []
def load(annotation_files):
    i = 0
    for a_file in annotation_files:
        print "Loading %s" % a_file
        a_dict = {}
        f = open(a_file, 'r')
        count = 0
        for line in f:
            r = line.split('\t')
            pmid = r[0]
            span_id = r[1]
            a_id = r[2]
            #, a_id, a_text) = line.split('\t')
            [pmid, span_id] = map(int, [pmid, span_id])
            if a_dict.has_key(span_id):
                a_dict[span_id] += " " + a_id
#                a_d = a_dict[span_id]
#                a_id_old = a_d[0]
#                a_text_old = a_d[1]
#                a_dict[span_id] = (a_id_old + " " + a_id, a_text_old + " " + a_text)
            else:
                a_dict[span_id] = a_id
#                a_dict[span_id] = (a_id, a_text)
            if count % 100000 == 0:
                print "%s - %s" % (field_names[i], count)
                
#            if count == 100000:
#                break;
            count +=1
                
        a_dicts.append((a_dict, field_names[i]))
        i +=1

def addAnnotations(doc, span_id):
    span_id = int(span_id)
    for (a_dict, field_name) in a_dicts:
        if a_dict.has_key(span_id):
            a_id = a_dict[span_id]
#             (a_id, a_text) = a_dict[span_id]
#            print "%s - %s - %s" % (field_name, a_id, span_id)
            doc.add(Field(field_name, a_id,
                      Field.Store.YES, Field.Index.TOKENIZED))
#            doc.add(Field(field_name+"_text", a_text,
#                      Field.Store.YES, Field.Index.TOKENIZED))        
#            doc.add(Field(field_name+"_text", a_text,
#                      Field.Store.YES, Field.Index.NO))        

def indexData(data_path):
    articles = glob.glob(os.path.join(data_path, '*'))
    nb_articles = len(articles)
    count = 0
    for article in articles:
        print "------------------ %s/%s ------------------" % (count, nb_articles)
        pmid = article.split('/')[-1]
        print pmid
        text = open(article, 'r').read()
        indexArticle(pmid, text)
        print "Tokenized and indexed"
        
#        if count == 500:
#            break;
        count +=1
            
p = re.compile('@#@#@ - (\d*) - @#@#@')
def indexArticle(pmid, text):
    res = p.split(text)
    i = 1
    for r in res[1::2]:
        span_id = r
        span_text = res[i+1] 
        try:
            doc = Document()
            doc.add(Field("span_id", span_id,
                          Field.Store.YES, Field.Index.UN_TOKENIZED))
            doc.add(Field("pmid", pmid,
                          Field.Store.YES, Field.Index.UN_TOKENIZED))
            doc.add(Field("text", span_text,
                          Field.Store.YES, Field.Index.TOKENIZED))
            addAnnotations(doc, span_id)
            writer.addDocument(doc)
        except Exception, e:
            sys.stderr.write("error: %s pmid: %s span_id: %s\n" % (e, pmid, span_id))
        i += 2

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Usage: python index_spans.py data_norm index_dir annotation_files"
    else:
        (data_norm, index_dir, annotation_files) = \
            (sys.argv[1], sys.argv[2], sys.argv[3:])
        print "Loading annotations ..."
        load(annotation_files)
        print "Making the index ..."
        writer = IndexWriter(index_dir, StandardAnalyzer(), True)
        writer.setMaxFieldLength(7 * 1000 * 1000 * 10)
        indexData(data_norm)
        print "Optimizing index ..."
        writer.optimize()
        print "Indexing complete"
        writer.close()
