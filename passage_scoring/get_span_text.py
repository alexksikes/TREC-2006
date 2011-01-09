import sys, os, re

DATA = "/projects/bebop/trec/trec2006/data.norm.new"
RES = "/projects/bebop/trec/trec2006/temp"

p = re.compile('@#@#@ - (\d*) - @#@#@')
def write_span_text(pmid, span_id):
    f = open(os.path.join(DATA, str(pmid)), 'r')
    text = f.read()
    
    res = p.split(text)
    i = 1
    for span_id_c in res[1::2]:
        if int(span_id_c) == span_id:
            f = open(os.path.join(RES, str(span_id)), 'w')
            f.write(res[i+1])
            f.close()
            return
        i += 2
    sys.stderr.write("No span text found for pmid = %s and span_id = %s\n" % (pmid, span_id))

def gsi(afile):
    lines = open(afile).readlines()
    r = []
    for line in lines:
        items = line.split("\t")
        r.append( (int(items[2]), int(items[0])) )
    return r   

def run(afile):
    r = gsi(afile)
    for (pmid, span_id) in r:
        write_span_text(pmid, span_id)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python get_span_text anna_file_detailed"
    else:
        run(sys.argv[1])
