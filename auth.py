from urlparse import urlparse
import hashlib


# return parsed URL
def parseURL(url):
	return urlparse(url)

# returns a dictionary of the parameters
def getParams(url):
	paramDict = {}
	params = url.query
	params = params.rsplit('&')
	
	for param in params:
		param = param.rsplit('=')
		paramDict[param[0]] = param[1]

	return paramDict

# returns the value of hash
def getHash(params):
	return params['hash']

url = 'http://northbridgetech.org/nexus/api/getUserGroups?userid=683&userloc=123&hash=62717d90f927f12919bac2949dea68e8d2e21a1e005c9435d9a339d71854bdd9'
location = url.find('hash')
urlLessHash = url[0:location-1]

secretTokenFile = open('secretToken.txt', 'r')
secretToken = secretTokenFile.read()
urlAndToken = urlLessHash + '&' + secretToken

hashObject = hashlib.sha256(urlAndToken.encode('utf-8'))
hexDig = hashObject.hexdigest()

parsedURL = parseURL(url)
params = getParams(parsedURL)
hashed = getHash(params)

if(hashed == hexDig):
	print('Success. Hash is valid')
else:
	print('Error. Hash is invalid')

