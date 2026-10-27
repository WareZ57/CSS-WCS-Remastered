import es
import playerlib
import wcs

def load():
	es.addons.registerClientCommandFilter(restrictedmap)

def unload():
	es.addons.unregisterClientCommandFilter(restrictedmap)

def restrictedmap(userid, args):
	if str(args[0]) == 'jointeam':
		race = wcs.wcs.getPlayer(userid).race.name
		
		raceinfo = wcs.wcs.racedb.getRace(race)

		curmap = es.ServerVar("eventscripts_currentmap")
		if curmap in raceinfo['restrictmap'].split('|'):
			es.tell(userid, "#multi", "#lightgreenSorry, #green%s #lightgreenis restricted on #green%s" % (race,curmap))
			return False
	return True