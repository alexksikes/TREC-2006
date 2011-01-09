import sys, getopt

from PyLucene import \
     Document, IndexSearcher, FSDirectory, QueryParser, StandardAnalyzer

def doQuery(searcher, flds, query, start, nb_results):
    parser = QueryParser("text", StandardAnalyzer())
    parser.setDefaultOperator(QueryParser.Operator.AND)
    query = parser.parse(query)
    hits = searcher.search(query)
    formatResultsTable(query, flds, hits, start, nb_results)

def formatResultsTable(query, flds, hits, start, nb_results):
    count = len(hits)
    for i in range(start,start+nb_results):
        if i == count:
            break
        doc = hits.doc(i)
        res = doc[flds[0]]
        for f in flds[1:]:
            res += '@#@#@'
            if doc.get(f):
                res += doc[f]
        print res
    
def usage():
    print "Run it on bebop using /projects/bebop/usr/local/bin/python"
    print """Usage: python r.py -i lucene_index -f field_mame_1,field_name_2,...,field_name_n -q 'the_query' -s start_page -r 
nb_of_results"""
    
def main(argv):                          
    # defaults
    query = ''
    start = 0
    nb_results = 10
    try:                                
        opts, args = getopt.getopt(argv, "i:f:q:s:r:", \
                   ["lucene_index=", "fields=", "query=", "start=", "nb_results="])
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
        elif opt in ("-f", "--fields"):      
            flds = arg.split(',')
        elif opt in ("-q", "--query"):      
            query = arg
        elif opt in ("-s", "--start"):                
            start = int(arg)
        elif opt in ("-r", "--nb_results"):
            nb_results = int(arg)
    doQuery(searcher, flds, query, start, nb_results)
    
if __name__ == "__main__":
    main(sys.argv[1:])
