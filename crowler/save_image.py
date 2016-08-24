__author__ = '_anboqing_'
import urllib2
import Image
import cStringIO
def ImageScale(url,size):
    file = cStringIO.StringIO(urllib2.urlopen(url).read())
    img = Image.open(file)
    img.show()

