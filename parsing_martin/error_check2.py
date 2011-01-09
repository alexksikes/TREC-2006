import os, re, sys, glob

# huge chunks
threshold = 100
count = 0

p = re.compile('\s+[0-9]+\s(.*)')
def huge_chunks(sections_clustered):
    global count
    
    lines = open(sections_clustered).readlines()
    for line in lines:
        m = p.match(line).group(1)
        if len(m) > threshold:
            count +=1
            print m
            print count

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python error_check2.py sections_clustered"
    else:
        huge_chunks(sys.argv[1])