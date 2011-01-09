# see how to supper treading mixin with pylucene
# see how to slice hits
# lucene uses a cache

import sys, re, urlparse, urllib

from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from Streams import StringReader

from PyLucene import \
     Document, IndexSearcher, FSDirectory, QueryParser, StandardAnalyzer, PythonThread, \
     Highlighter, QueryScorer, SimpleAnalyzer, SimpleHTMLFormatter, SimpleFragmenter

SERVER_PORT = 8765

def doQuery(query, start, nb_results):
    parser = QueryParser("text", StandardAnalyzer())
    parser.setDefaultOperator(QueryParser.Operator.AND)
    query = parser.parse(query)
    hits = searcher.search(query)
    
    return formatResultsPlain(query, hits, nb_results, start)

def formatResultsPlain(query, hits, nb_results, start):
#    # for highlighting
#    scorer = QueryScorer(query)
#    #formatter = SimpleHTMLFormatter("<span class=\"highlight\">", "</span>")
#    highlighter = Highlighter(scorer)
#    fragmenter = SimpleFragmenter(50 * 1000 * 1000)
#    highlighter.setTextFragmenter(fragmenter)
    
    # format the result "count | span_id1:pmid:text span_id2:pmid:text ..."
    count = len(hits)
    res = "%s||@||" % count
    for i in range(start,start+nb_results):
        if i > count - 1:
            break
        doc = hits.doc(i)
        
#        title = doc['text']
#        stream = StandardAnalyzer().tokenStream('text', StringReader(title))
#        fragment = highlighter.getBestFragment(stream, title)
#        print doc['text']
#       
        # because xml wrapper for php not installed
        # we have to do this mess
        sect = ""
        gene = ""
        if doc.get('section'):
            sect = doc['section']
        if doc.get('gene'):
            gene = doc['gene']
        res += "##@##%s::@::%s::@::%s::@::%s::@::%s" % \
            (doc['span_id'], doc['pmid'], sect, gene, doc['text'])
    return res

def formatResultsXML(hits, nb_results, start):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += "<ResultSet totalResultsAvailable=\"%s\" totalResultsReturned=\"%s\" firstResultPosition=\"%s\">\n" % (len(hits), nb_results, start)
    for i, doc in hits:
        if i == nb_results:
            break;
        xml += "<Result><SpanId>%s</SpanId><Pmid>%s</Pmid><Text>%s</Text></Result>\n" % \
            (doc['span_id'], doc['pmid'], doc['text'])
    xml += "</ResultSet>"
    return xml        

class SearchRequestHandler(BaseHTTPRequestHandler):
    p = re.compile('query=(.+)&start=(\d+)&results=(\d+)')
    def _writeheaders(self, doc):
        self.send_response(200)
        self.send_header('Content-type', 'text/xml')
        self.end_headers()
    
    def _getdoc(self, filename, args):
        doc = "0 |"
        m = self.__class__.p.search(args)
        if m and filename == '/search':
        #    doc = doQuery(m.group(1).split('+'), int(m.group(2)), int(m.group(3)))
            doc = doQuery(urllib.unquote(m.group(1)), int(m.group(2)), int(m.group(3)))
        return doc
        
    def do_GET(self):
        url = urlparse.urlsplit(self.path)
        doc = self._getdoc(url[2], url[3])
        self._writeheaders(doc)
        self.wfile.write(doc)
                
class SearchServer(HTTPServer):
    allow_reuse_address = 1

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python lucene_server.py index_dir"
    else:
        indexDir = sys.argv[1]
        fsDir = FSDirectory.getDirectory(indexDir, False)
        searcher = IndexSearcher(fsDir)
        
        serveraddr = ('', SERVER_PORT)
        srvr = SearchServer(serveraddr, SearchRequestHandler)
        print "Ready to serve search queries"
        srvr.serve_forever()
