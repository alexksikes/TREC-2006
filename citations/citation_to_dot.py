import sys

def run(c, d):
    d.write(
"""graph G  {
        //size="7,10"
        //page="8.5,11"
        //center=""
        node[shape=point]\n""")
    
    for l in c.readlines():
        d.write("\t" + " -- ".join(l.split()) + "\n")
    
    d.write("}")
    d.close()
    c.close()
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: python citation_to_dot.py citation_file dot_file"
    else:
        c = file(sys.argv[1], 'r')
        d = file(sys.argv[2], 'w')
        run(c, d)    
