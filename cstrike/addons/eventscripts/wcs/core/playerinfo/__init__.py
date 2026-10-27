import es
from popuplib import easymenu, create
import playerlib
import wcs

popups = []


def doCommand(userid):
	if es.exists('userid', userid):
		pname = 'playerinfo'+str(userid)
		popups.append(pname)
		popup = easymenu(pname, '_popup_choice', callBack)
		popup.settitle('Page')

		popup.c_beginsep = None
		popup.c_pagesep = None

		for user in es.getUseridList():
			popup.addoption(user, es.getplayername(user))

		popup.send(userid)
		es.ServerVar('wcs_ppuser').set(userid)
		es.doblock("pending/pending")

def popupHandler(userid, target, popupid):
	if es.exists('userid', target):
		pname = 'playerinfo1'+str(userid)
		popups.append(pname)
		popup = create(pname)
		popup.menuselect = playerinfoselection
		index = float(es.getindexfromhandle(es.getplayerhandle(target)))
		gravity = float(es.entitygetvalue(index, "gravity"))
		health = playerlib.getPlayer(target).getHealth()
		speed = playerlib.getPlayer(target).getSpeed()
        	color = playerlib.getPlayer(target).getColor()
		a,b,c,d = color
		player = wcs.wcs.getPlayer(target)
		popup.addline('->1. '+str(es.getplayername(target)))
		popup.addline('-'*25)
		popup.addline('o Total level '+str(player.player.totallevel))
		popup.addline('-'*25)
		popup.addline('o '+str(player.player.currace)+': Level '+str(player.race.level))

		race = wcs.wcs.racedb.getRace(player.player.currace)
		name = race['skillnames'].split('|')
		skills = player.race.skills.split('|')
		player = wcs.wcs.getPlayer(target)
		race = player.player.currace
		raceinfo = wcs.wcs.racedb.getRace(race)
		levels = int(raceinfo['numberoflevels'])
		for skill, level in enumerate(skills):
			popup.addline(' - '+name[skill]+': ['+str(level)+'/'+str(levels)+']')

		popup.addline('-'*25)
		popup.addline('Health : '+str(health))
		popup.addline('Invisibility : '+str(round(100-d/2.55))+'% ')
		popup.addline('Speed : '+str(round(speed*100))+'% ')
		popup.addline('Gravity : '+str(gravity*100)+'% ')
		popup.addline('-'*25)

		popup.addline('->8. Previous')
		popup.addline(' ')
		popup.addline('0. Close')

		for x in xrange(1, 8):
			popup.submenu(x, pname)

		popup.submenu(9, pname)

		popup.send(userid)
		es.ServerVar('wcs_ppuser').set(userid)
		es.doblock("wcs/tools/pending/pending")
	else:
		es.tell(userid, 'Unknown player')
		doCommand(userid)

def playerinfoselection(userid, choice, popupid):
	if choice == 8:
		doCommand(userid)


callBack = popupHandler

def getPopups():
	return popups