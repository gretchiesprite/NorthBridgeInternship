import string, time, math, random
import hashlib

def newUuid(): 
    s = hashlib.md5(uniqid(random.randint(0, 2147483647), True)).hexdigest().lower() 
    guidText = s[0:8] + '-' + s[8:12] + '-' + s[12:16] + '-' + s[16:20] + '-' + s[20:]
    return guidText

#From http://gurukhalsa.me/2011/uniqid-in-python/
def uniqid(prefix='', more_entropy=False):
    m = time.time()
    uniqid = '%8x%05x' %(math.floor(m),(m-math.floor(m))*1000000)
    if more_entropy:
        valid_chars = list(set(string.hexdigits.lower()))
        entropy_string = ''
        for i in range(0,10,1):
            entropy_string += random.choice(valid_chars)
        uniqid = uniqid + entropy_string
    uniqid = str(prefix) + uniqid
    return uniqid

def getDemoNowEvent():
	return DEMO_EVENT_NOW

def getDemoFutureEvent():
	return DEMO_EVENT_FUTURE