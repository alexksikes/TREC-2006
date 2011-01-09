# TODO:
# - keep connection instead fo making a new one each time
# - test with concurrent connections

import socket, sys, time, urllib, getopt
#import MySQLdb

#table = "talks_scraped"
#db = MySQLdb.connect(host="localhost", user="alex", passwd="passwd", db="db")
#cursor = db.cursor()
    
def test_server(cmd, start, nb_results, nb_times):
    while 1:
        print "--------------------------------------"
        print "Your query: ", 
        query = sys.stdin.readline()
        query = query.split()
        query = '+'.join(query)
        print
        print "Running your query %s times" % nb_times
        
        clock1 = time.time()
        for i in range(nb_times):
           url = "http://localhost:8765/%s?query=%s&start=%s&results=%s" % (cmd, query, start, nb_results)
           res = urllib.urlopen(url).read()
        clock2 = time.time()
        print "It took %s sec total (including count)" % (clock2 - clock1)
        print "--------------------------------------"
        print res
        print 
        
        # parse output
        if res:
            t = res.split("|")
            count = t[0].strip()
            ids = t[1].split()
            
#            # display
#            if cmd == 'search':
#                print "%s total results found" % count
#                print "Top %s sorted by freshness:" % nb_results
#                print
#                if ids:
#                    query = "SELECT description, url FROM %s WHERE id=%s" % (table, ids[0])
#                    for id in ids[1:]:
#                        query += " OR id=%s" % id.strip()
#                    clock1 = time.time()
#                    cursor.execute(query)
#                    results = cursor.fetchall()
#                    clock2 = time.time()
#                    for result in results:
#                        print result[0]
#                        print result[1]
#                    print
#                    print "The mySQL query took %s sec" % (clock2 - clock1)
#            else:
#                print "%s total tags found" % count
#                print "Top %s tags sorted by counts:" % nb_results
#                print
#                for id in ids:
#                    print id
                
def usage():
    print """Usage: python test_server.py -q -c -s [start_page_nb] -r 
[nb_of_results] -t [nb_times_todo_query] [-h]"""
    
def main(argv):                          
    # defaults
    cmd = 'search'
    query = ''
    start = 0
    nb_results = 10
    nb_times = 1
    
    try:                                
        opts, args = getopt.getopt(argv, "hqcs:r:t:", 
                ["help", "query=", "cloud=", "start=", "nb_results=", "nb_times="])
    except getopt.GetoptError:          
        usage()                         
        sys.exit(2)                     
    if not opts:
        usage()
        sys.exit()
    
    for opt, arg in opts:                
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-q", "--query"):      
            cmd = 'search'
        elif opt in ("-c", "--cloud"):      
            cmd = 'cloud'
        elif opt in ("-s", "--start"):                
            start = arg
        elif opt in ("-r", "--nb_results"):                
            nb_results = int(arg)
        elif opt in ("-t", "--times"):                
            nb_times = int(arg)
    test_server(cmd, start, nb_results, nb_times)
    
if __name__ == "__main__":
    main(sys.argv[1:])
