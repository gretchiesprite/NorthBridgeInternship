from urlparse import urlparse
import hashlib
import requestInterface

# returns a dictionary of the parameters
def get_params(url):
	paramDict = {}
	params = url.query
	params = params.rsplit('&')
	
	for param in params:
		param = param.rsplit('=')
		paramDict[param[0]] = param[1]

	return paramDict

# returns the value of hash
def get_hash(params):
	if 'hash' in params:
		return params['hash']
	else:
		return None

def main():
	url = 'http://northbridgetech.org/nexus/api/getUsers?userid=127&username=kdf&hash=1730f055ae25a08d71f52772f1b9517aa642b67706d02af10a953d2b6e8509cb'
	location = url.find('hash')
	urlLessHash = url[0:location-1]

	secretTokenFile = open('secretToken.txt', 'r')
	secretToken = secretTokenFile.read()
	urlAndToken = urlLessHash + '&' + secretToken

	hashObject = hashlib.sha256(urlAndToken.encode('utf-8'))
	hexDig = hashObject.hexdigest()

	parsedURL = urlparse(url)
	params = get_params(parsedURL)
	hashed = get_hash(params)

	function = parsedURL.path[11:]

	if (hashed == None):
		print('Hash not found. URL is invalid.')
	elif(hashed == hexDig):
		print('Success. Hash is valid.')
		requestInterface.get_request(function, params)
	else:
		print('Error. Hash is invalid.')

if __name__ == "__main__":
	main()


