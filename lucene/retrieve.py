import sys, getopt

from PyLucene import \
     Document, IndexSearcher, FSDirectory, QueryParser, StandardAnalyzer

def doQuery(searcher, query, start, nb_results):
    parser = QueryParser("text", StandardAnalyzer())
    parser.setDefaultOperator(QueryParser.Operator.AND)
    query = parser.parse(query)
    hits = searcher.search(query)
    formatResultsTable(query, hits, nb_results, start)

def formatResultsTable(query, hits, nb_results, start):
    count = len(hits)
    for i in range(start,start+nb_results):
        if i > count - 1:
            break
        doc = hits.doc(i)
        sect = gene = ""
        if doc.get('section'):
            sect = doc['section']
        if doc.get('gene'):
            gene = doc['gene']
        print "%s@#@#@%s@#@#@%s@#@#@%s@#@#@%s" % \
            (doc['span_id'], doc['pmid'], sect, gene, doc['text'])
    
def usage():
    print "Run it on bebop using /projects/bebop/usr/local/bin/python"
    print """Usage: python retrieve.py -i lucene_index -q 'the_query' [-s start_page] [-r 
nb_of_results]"""
    
def main(argv):                          
    # defaults
    query = ''
    start = 0
    nb_results = 10
    try:                                
        opts, args = getopt.getopt(argv, "i:q:s:r:", \
                   ["lucene_index=", "query=", "start=", "nb_results="])
    except getopt.GetoptError:          
        usage()                         
        sys.exit(2)                     
    if not opts:
        usage()
        sys.exit()
    for opt, arg in opts:                
        if opt in ("-i", "--lucene_index"):      
            fsDir = FSDirectory.getDirectory(arg, False)
            searcher = IndexSearcher(fsDir)
        elif opt in ("-q", "--query"):      
            query = arg
        elif opt in ("-s", "--start"):                
            start = int(arg)
        elif opt in ("-r", "--nb_results"):
            nb_results = int(arg)
    doQuery(searcher, query, start, nb_results)
    
if __name__ == "__main__":
    main(sys.argv[1:])
