import sys, os, re
from score_passage import *

DATA = "/projects/bebop/trec/trec2006/data.norm.new"
RESULTS = "/projects/bebop/trec/trec2006/results"

p = re.compile('@#@#@ - (\d*) - @#@#@')
def get_span_text(pmid, span_id):
    text = open(os.path.join(DATA, str(pmid)), 'r').read()
    
    res = p.split(text)
    i = 1
    for span_id_c in res[1::2]:
        if int(span_id_c) == span_id:
            return res[i+1]
        i += 2
    sys.stderr.write("No span text found for pmid = %s and span_id = %s\n" % (pmid, span_id))
    return None
    
def gsi(afile):
    lines = open(afile).readlines()
    r = []
    for line in lines:
        items = line.split("\t")
        r.append( (int(items[2]), int(items[0]), items[1]) )
    return r  

def run(afile, fout):
    out = open(fout, 'w')
    r = gsi(afile)
    for (pmid, span_id, q_id) in r:
        span_text = get_span_text(pmid, span_id)
        if span_text:
            out.write("%s\t%s\t%s\t%s\n" % (span_id, q_id, pmid, score(q_id, span_text)))
    out.close()

def run_all(out_folder):
    for i in range(188)[160:188]:
        print i
        run(os.path.join(RESULTS, "results_%s/complete_%s" % (i, i)), 
            os.path.join(out_folder, "%s.results" % i) )
        
if __name__ == '__main__':
#    if len(sys.argv) != 3:
#        print "Usage: python score_all_passages.py anna_file_detailed output_file"
#    else:
#        run(sys.argv[1], sys.argv[2])
    if len(sys.argv) != 2:
        print "Usage: python score_all_passages.py out_folder"
    else:
        run_all(sys.argv[1])
