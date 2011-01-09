import os, re, sys, glob

SPANS = "/projects/bebop/trec/trec2006/spans_id.txt"
RESULTS = "/projects/bebop/trec/trec2006/alternatives"
OUT = "/projects/bebop/trec/trec2006/results_with_pmids"

d = {}
def load_spans():
    print "Loading %s" % SPANS
    count = 0
    f = open(SPANS, 'r')
    for line in f:
        r = line.split('\t')
        span_id = int(r[0])
        pmid = int(r[1])
        d[span_id] = pmid
        if count % 100000 == 0:
            print " -- %s -- " % span_id
        count +=1

def write_file(results_f, out_f):
    print "Writting %s" % out_f
    out = open(out_f, 'w')
    lines = open(results_f, 'r').readlines()
    for line in lines:
        span_id = int(line.split("\t")[0])
#        print "%s\t%s" % (span_id, d[span_id])
        out.write("%s\t%s\n" % (span_id, d[span_id]))
    out.close()

def run():
    load_spans()
    for i in range(188)[161:188]:
        write_file(os.path.join(RESULTS, "results_%s/span_ids_%s" % (i, i)),  
                os.path.join(OUT, "results_%s" % i))
        
if __name__ == '__main__':
    if len(sys.argv) == 0:
        print "Usage: python span_ids_to_pmids"
    else:
        run()
