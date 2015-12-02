import event

def parse_request(request, all_params):
	if(request == 'isValidMeetingType'):
		event.is_valid_meeting_type(all_params)
	elif(request == 'getFutureEvents'):
		event.get_future_events(all_params)
	elif(request == 'addEvent'):
		event.add_event(all_params)
	elif(request == 'deleteEvent'):
		event.delete_event(all_params)
	elif(request == 'updateDemoNowEvent'):
		event.update_demo_now_event(all_params)
	elif(request == 'updateDemoFutureEvent'):
		event.update_demo_future_event(all_params)
	else:
		print('not a valid request')