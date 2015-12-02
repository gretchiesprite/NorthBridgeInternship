import eventInterface
#import organizationInterface
#import groupInterface
#import scheduleInterface
#import invitationInterface
#import userInterface

def get_request(request, all_params):
	if('Event' in request):
		eventInterface.parse_request(request, all_params)
	elif('Organization' or 'organization' in request):
		print('Organization Request')
		#oranizationInterface.parse_request(request, all_params)
	elif('Group' or 'group' in request):
		print('Group Request')
		#groupInterface.parse_request(request, all_params)
	elif('Schedule' in request):
		print('Schedule Request')
		#scheduleInterface.parse_request(request, all_params)
	elif('Invitation' in request):
		print('Invitation Request')
		#invitationInterface.parse_request(request, all_params)
	elif('User' in request):
		print('User Request')
		#userInterface.parse_request(request, all_params)
	else:
		print('Not a valid request')