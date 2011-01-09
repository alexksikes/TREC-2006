import sys, os, re

p = re.compile('<p>|</p>|<p .*?>', re.IGNORECASE)
def compute_spans(span_id, pmid, html):
    spans = []
    pos = 0
    for m in p.finditer(html):
        block = html[pos:m.start()]
        size = len(block)
        if size > 0: 
            spans.append((span_id, pmid, pos, size, block))
            span_id += 1
        pos = m.end()
    block = html[pos:]
    size = len(block)
    if size > 0: 
        spans.append((span_id, pmid, pos, size, block))
    return spans

delim = '@#@#@'
def write_spans(spans, span_file=None, block_file=None, normalizer=None):
    s = ""
    b = ""
    for (span_id, pmid, pos, size, block) in spans:
        if normalizer:
            try:
                block = normalizer(block)
            except Exception, e:
                sys.stderr.write("Error on file: %s\n" % pmid)
                sys.stderr.write(e + '\n')
        s += '%s\t%s\t%s\t%s\n' % (span_id, pmid, pos, size)
        b += '%s - %s - %s%s' % (delim, span_id, delim, block)
    if span_file:
        span_file.write(s)
        block_file.write(b)
    else:
        print s,
        print b,
        
def run(article):
    f = open(article, 'r')
    pmid = re.sub('.html|.htm', '', os.path.split(f.name)[1])
    spans = compute_spans(0, pmid, f.read())
    write_spans(spans)
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python compute_spans.py html_file"
    else:
        run(sys.argv[1])
