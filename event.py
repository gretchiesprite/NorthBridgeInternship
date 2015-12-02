import psycopg2
from psycopg2 import extras
import json

class Event:
	#TODO: read in config_env to get db host, name, and user
	dbHost = "localhost"
	dbUser = "northbr6_web"
	dbName = "localnexus"

	def _ps_execute(query, input):
		#result = prepare = FALSE
		conn = psycopg2.connect('dbname={} user={} host={}'.format(dbName, dbUser, dbHost))
		cur = conn.cursor()
		result = cur.execute(query)
		#pgDb::disconnect(con)
		#if (not result) {
			trigger_error('Cannot execute query: {}\n'.format(query), E_USER_ERROR)
		return result
	
	def _get_day(day):
		dayMap = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
		if (day in dayMap):
			return dayMap[day]
		return 'undefined'
	
	def _get_month(month):
		monthMap = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		if (month in monthMap):
			return monthMap[month]
		return 'undefined'
	
	def _get_hour(hour):
		if (1 <= hour and hour < 13):
			return hour
		elif (13 <= hour and hour < 24):
			return hour-12
		elif (0 == hour):
			return '12'
		else:
			return 'undefined'
	
	def _get_minute(minute):
		if (0 <= minute and minute < 10):
			return '0' + minute
		else:
			return minute
	
	def _get_period(period):
		if (0 <= period and period < 13):
			return 'AM'
		elif (13 <= period and period < 24):
			return 'PM'
		else:
			return 'undefined'
	
	def _get_meeting_type_display(typeDisplay):
		#TODO - should leverage the constants defined in BbbMEeting.php. This is duplicated stringage
		if (typeDisplay == 'video tether'):
			return 'Video Link'
		elif (typeDisplay == 'video chat'):
			return 'Video Chat'
		elif (typeDisplay == 'webinar'):
			return 'Webinar'
		else:
			return 'Collaboration'

	def is_valid_time_zone(timeZone):
		query = """SELECT exists (SELECT name FROM pg_timezone_names WHERE name = (%s));"""
		params = (timeZone,)		
		row = fetchone(event._ps_execute(query, params)
		if (row[0] != "t"):
			return TRUE
		return FALSE
	
	def is_valid_meeting_type(meetingType):
  		query = """SELECT exists (SELECT e.enumlabel FROM pg_type t, pg_enum e 
  			WHERE t.oid = e.enumtypid
  			AND t.typname like 'meeting%'
  			AND e.enumlabel = (%s));"""
		params = (meetingType,)
  		row = fetchone(event._ps_execute(query, params))
		if (row[0] != "t"):
			return TRUE
		return FALSE
	
	#Added default value for ssnUser so as to not have to change the order
	def get_future_events(groupId, localTz = "Greenwich", ssnUser = 000000000):
		# do I really need to initialize this as an empty tuple/list?
		events = ()
		if (self.isValidTimeZone(localTz)):
			query = """SELECT
				extract(day FROM (SELECT e.start_dttm at time zone %(ltz)s)) AS date, 
				extract(dow FROM (SELECT e.start_dttm at time zone %(ltz)s)) AS day, 
				extract(month FROM (SELECT e.start_dttm at time zone %(ltz)s)) AS month, 
				extract(hour FROM (SELECT e.start_dttm at time zone %(ltz)s)) AS hour, 
				extract(minute FROM (SELECT e.start_dttm at time zone %(ltz)s)) AS minute, 
				extract(epoch FROM (SELECT e.start_dttm)) AS epoch,
				e.tz_name AS tzname, 
				e.duration AS duration, 
				e.name AS name, 
				e.descr AS descr, 
				e.uuid AS uuid,
				e.reserved_user_fk AS adder,
				e.type AS meetingtype,
				u.fname AS fname, 
				u.lname AS lname,
				pg.abbrev AS abbrev 
			FROM event e, public.user u, pg_timezone_names pg
			WHERE e.group_fk = %(gid)s		
			AND (e.start_dttm + e.duration) > now() 
			AND e.active = true
			AND pg.name = %(ltz)s
			AND u.id = e.reserved_user_fk 
			ORDER BY e.start_dttm"""

			params ={'gid': groupId, 'ltz': localTz}

			cursor = event._ps_execute(query, params)
			counter = 0
			while (row = fetchmany(cursor)): #http://initd.org/psycopg/docs/cursor.html#cursor.fetchmany
				events[counter]['date'] = row['date']
				events[counter]['day'] = self._get_day(row['day'])
				events[counter]['month'] = self._get_month(row['month']-1)
				events[counter]['hour'] = self._event__get_hour(row['hour'])
				events[counter]['minute'] = self._event__getMinute(row['minute'])
				events[counter]['epoch'] = row['epoch']
				events[counter]['period'] = self._event__get_period(row['hour'])
				events[counter]['abbrev'] = row['abbrev']
				events[counter]['purpose'] = row['name']
				events[counter]['descr'] = row['descr']
				events[counter]['uuid'] = row['uuid']
				events[counter]['mtype'] = row['meetingtype']
				events[counter]['mtypdisplay'] = self._event__get_meeting_type_display(row['meetingtype'])
				events[counter]['fname'] = row['fname']
				events[counter]['lname'] = row['lname']
				events[counter]['sessionUser'] = ssnUser
				events[counter]['adder'] = row['adder']
				counter++
		return events
	
	def add_event(dttm, duration, name, reservedUserId, groupId, tzName, type, descr, loc, isBbb):
		query = """SELECT abbrev FROM pg_timezone_names WHERE name = (%s)"""
		params = (tzName,) 
		row = fetchone(event._ps_execute(query, params)
		tzAbbrev = row[0]

		query = """INSERT INTO event (uuid, start_dttm, duration, name, descr, reserved_user_fk, group_fk, tz_name, tz_abbrev, type) VALUES (%s, %s, 3, 4, 9, 5, 6, 7, 8, 10)"""
		#TODO - Need to write newUUid function
		params = (Util.newUUid(), dttm, duration, name, loc, reservedUserId, tzname, tzAbbrev, descr, type, isBbb)
		event._ps_execute(query, params)
		return
	
	def delete_event(uuid):
		query = """UPDATE event SET active = false WHERE uuid = 1"""
		event._ps_execute(query, ())
		return
	
	def update_demo_now_event():
		query = """UPDATE event SET start_dttm = (now() - interval '5 minutes') WHERE id = '" + Util.getDemoNowEvent() + "'"""
		event._ps_execute(query, ())
		return
	
	def update_demo_future_event():
		query = """UPDATE event SET start_dttm = (start_dttm + interval '1 week') WHERE id IN (" + Util.getDemoFutureEvent() + ")"""
		event._ps_execute(query, ())
		return

