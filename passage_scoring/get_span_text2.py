import sys, os, re

DATA = "/projects/bebop/trec/trec2006/data.norm.new"

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

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: python get_span_text pmid span_id"
    else:
        print get_span_text(int(sys.argv[1]), int(sys.argv[2]))
