import DB2, sys, os, re

conn = DB2.connect(dsn='db', uid='uid', pwd='pwd')
c = conn.cursor()
c.execute('SET SCHEMA db2inst1')
DEST = "."

def read_pmid_file(pmids_f):
    lines = open(pmids_f, 'r').readlines()
    bundle = []
    pmids = []
    for (i, l) in enumerate(lines):
        pmids.append(l)
        if (i + 1) % 1000 == 0:
            bundle.append(pmids)
            pmids = []
    if pmids:
        bundle.append(pmids)
    return bundle

descriptor = {}
def load_mesh_descriptors():
    q = """select distinct mdtn.tree_number, md.descriptor_name
            from mesh_term_string_to_descriptor_ui AS mtstd 
            join mesh_desc_tree_number AS mdtn on mtstd.descriptor_ui = mdtn.descriptor_ui
            join mesh_descriptor AS md on md.descriptor_ui = mdtn.descriptor_ui"""
    c.execute(q)

    rows = c.fetchall()
    count, total = 0, len(rows)
    for (tree_number, descriptor_name) in rows:
        if (count % 10000 == 0):
            print "%s / %s" % (count, total)
        descriptor[tree_number] = descriptor_name
        count +=1
    
def get_categories(tree_number):
    trees, categories = [], [] 
    for t in tree_number.split('.'):
        trees.extend([t])
        categories.append(descriptor[".".join(trees)])
    return categories

mesh_top = \
{'A':'Anatomy',
'B':'Organisms',
'C':'Diseases',
'D':'Chemicals and Drugs',
'E':'Analytical, Diagnostic and Therapeutic Techniques and Equipment',
'F':'Psychiatry and Psychology',
'G':'Biological Sciences',
'H':'Physical Sciences',
'I':'Anthropology, Education, Sociology and Social Phenomena',
'J':'Technology and Food and Beverages',
'K':'Humanities',
'L':'Information Science',
'M':'Persons',
'N':'Health Care',
'V':'Publication Characteristics',
'Z':'Geographic Locations'}
def get_top_category(tree_number):
    return mesh_top[tree_number[:1]]

def normalize(category_name):
    category_name = re.sub(' ', '_', category_name)
    category_name = re.sub(',', '', category_name)
    # mysql will error if flamenco table is too long
    if len(category_name) > 60:  
        category_name = category_name.split('_')[0]
    return category_name.lower()
#    return category_name.split()[0].lower()
    
def make_facets(pmid_qs):
    term_id = 0
    facet_f = open(os.path.join(DEST, 'facets.tsv'), 'w')

    for pmid_q in pmid_qs:
        q = """select distinct mc.pmid, mdtn.tree_number
            from medline_citation AS mc 
            join medline_mesh_heading AS mmh on mc.pmid = mmh.pmid
            join mesh_term_string_to_descriptor_ui AS mtstd on mmh.descriptor_name = mtstd.term_string
            join mesh_desc_tree_number AS mdtn on mtstd.descriptor_ui = mdtn.descriptor_ui
            where mc.pmid in (%s)""" % ",".join(pmid_q)
        c.execute(q)
        
        row = c.fetchone()
        while row:
            (pmid, tree_number) = row
            top = get_top_category(tree_number)
            hierarchy = get_categories(tree_number)
            facet = normalize(top)
            
            write_facets(facet_f, facet, top, top)
            write_facet_terms(facet, term_id, hierarchy)
            write_facet_map(facet, pmid, term_id)
            
            if (term_id % 10000 == 0):
                print "%s / %s" % (term_id, 630000)
            
            row = c.fetchone() # bug in db2.py, have to use fetchone()
            term_id +=1

def make_items(pmid_qs):
    s = "\n".join(["pmid\tpmid", "title\tTitle", "urll\turl"])
    open(os.path.join(DEST, 'attrs.tsv'), 'w').write(s+"\n")
        
    items_f = open(os.path.join(DEST, 'items.tsv'), 'w')
    text_f = open(os.path.join(DEST, 'text.tsv'), 'w')
    count = 0
    
    for pmid_q in pmid_qs:
        q = """select mc.pmid, mc.article_title
            from medline_citation AS mc 
            where mc.pmid in (%s)""" % ",".join(pmid_q)
        c.execute(q)
        
        rows = c.fetchall()
        total = len(rows)
        for (pmid, title) in rows:
            url = "http://www.ncbi.nlm.nih.gov/entrez/queryd.fcgi?cmd=Retrieve&db=pubmed&dopt=Abstract&list_uids=%s&itool=pubmed_docsum" % pmid
            
            items_f.write("%s\t%s\t%s\t%s\n" % (pmid, pmid, title, url))
            text_f.write("%s\t%s\n" % (pmid, title.lower()))
            
            if (count % 10000 == 0):
                print "%s / %s" % (count, total)
            count +=1

def write_facets(facets_f, facet, short_name, long_name):
    if not facet_terms_f.has_key(facet):
        facets_f.write("%s\t%s\t%s\n" % (facet, short_name, long_name))
        facet_terms_f[facet] = open(os.path.join(DEST, facet+'_terms.tsv'), 'w')
        facet_map_f[facet] = open(os.path.join(DEST, facet+'_map.tsv'), 'w')

facet_terms_f = {}
def write_facet_terms(facet, term_id, hierarchy):
    facet_terms_f[facet].write("%s\t%s\n" % (term_id, "\t".join(hierarchy)))

facet_map_f = {}
def write_facet_map(facet, item_id, term_id):
    facet_map_f[facet].write("%s\t%s\n" % (item_id, term_id))
    
def run(pmids, instance_folder):
    global DEST
    DEST = os.path.abspath(instance_folder)
    print "Reading pmid file ..."
    pmid_query = read_pmid_file(pmids)
    print "Loading mesh descriptors ..."
    load_mesh_descriptors()
    print "Making the facets ..."
    make_facets(pmid_query)
    print "Making items ..."
    make_items(pmid_query)
    print "Trec instance at %s complete" % DEST
        
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: python %s pmid_file instance_folder" % sys.argv[0]
    else:
        run(sys.argv[1], sys.argv[2])
    c.close()
    conn.close()
