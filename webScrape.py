import urllib2
from bs4 import BeautifulSoup
from threading import Thread
import time
import re
class myThread (Thread):
    def __init__(self,name,delay):
        Thread.__init__(self)
        self.name = name
        self.delay=delay
    def run(self):
        for i in range(10):
            print self.name +" "+str(i)
            time.sleep(self.delay)

class Queue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def enqueue(self,item):
        self.items.insert(0,item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)

visited = []
bad = []
workQueue = Queue()
workQueue.enqueue("http://www.realclearpolitics.com")
while(not workQueue.isEmpty()):
    url = workQueue.dequeue()
    print url
    if url not in visited and url not in bad:
        try:
            response = urllib2.urlopen(url)
            visited.append(url)
            html = response.read()
            print len(html)
            response.close()
            soup = BeautifulSoup(html,'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if(href != None):
                    if(href.startswith("http")):
                        workQueue.enqueue(href)
                    elif(href.startswith("/")):
                        baseUrl = re.search(r'^.+?[^\/:](?=[?\/]|$)', url).group(0)
                        workQueue.enqueue(baseUrl+href)
                #ignore the rest as unrecognzied
            while(not workQueue.isEmpty()):

                print workQueue.dequeue()
            break
        except urllib2.URLError:
            bad.append(url)



#todo

#get stop conditions and let it recurse
#figure out what to write and let a thread do it
def makeThreads():
    thread1 = myThread("thread1",1)
    thread2 = myThread("thread2",2)

    thread1.start()
    thread2.start()

    thread2.join()
    thread1.join()

    print "done"
