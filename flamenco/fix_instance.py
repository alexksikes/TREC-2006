import sys, os, glob, re

descriptors = {}
def load_terms(terms):
    global descriptors
    lines, descriptors = open(terms, 'r').readlines(), {}
    for (count, l) in enumerate(lines):
        r = l.split('\t')
        term_id = r[0]
        categories = "\t".join(r[1:])[:-1]
        if descriptors.has_key(categories):
            descriptors[categories].append(term_id)
        else:
            descriptors[categories] = [term_id]
        show_progress(count, len(lines), 100000)
    
item_ids = {}
def load_map(map):
    global item_ids
    lines, item_ids = open(map, 'r').readlines(), {}
    for (count, l) in enumerate(lines):
        r = l.split('\t')
        item_id = r[0]
        term_id = r[1][:-1]
        item_ids[term_id] = item_id
        show_progress(count, len(lines), 100000)
    
def write(dest, filename):
    terms_f = open(os.path.join(dest, filename+'_terms.tsv.fixed'), 'w')
    map_f = open(os.path.join(dest, filename+'_map.tsv.fixed'), 'w')
    for (id, d) in enumerate(descriptors):
        terms_f.write("%s\t%s\n" % (id, d))
        for term_id in descriptors[d]:
            map_f.write("%s\t%s\n" % (item_ids[term_id], id))
        show_progress(id, len(descriptors), 10000)
    terms_f.close()
    map_f.close()
    
def get_facet_names(dest):
    r = []
    for terms in glob.glob(os.path.join(dest, '*_terms.tsv')):
        facet_name = re.sub('_terms.tsv', '', os.path.split(terms)[1])
        r.append(facet_name)
    return r

def show_progress(count, total, inc):
    if (count % inc == 0):
        print "%s / %s" % (count, total-1)

def run(dest):  
    facets = get_facet_names(dest)
    for (count, facet) in enumerate(facets):
        print "------------------------------------------------"
        print "****** %s ******" % facet
        show_progress(count, len(facets), 1)
        print "------------------------------------------------"
        
        terms = os.path.join(dest, facet+'_terms.tsv')
        print "Loading %s" % terms
        load_terms(terms)
        
        map = os.path.join(dest, facet+'_map.tsv')
        print "Loading %s" % map
        load_map(map)
        
        print "Writting fixed intance in .fixed files"
        write(dest, facet)
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python %s instance_folder" % sys.argv[0]
    else:
        run(sys.argv[1])
            