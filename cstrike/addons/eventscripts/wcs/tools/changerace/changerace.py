import es
import wcs
import cmdlib

def load():
	cmdlib.registerServerCommand('wcs_change_race', wcs_change_race, 'Will change a players race')


def wcs_change_race(args):
	if len(args) != 2:
		es.dbgmsg(0, "Syntax Error: Wrong amount of arguments.")
	if len(args) == 2:
		userid = args[0]
		race = args[1]
		wcs.wcs.getPlayer(userid).changeRace(race)
		wcs.wcs.tell(userid, 'changerace: change race', {'race':race})
		
	
def unload():
	cmdlib.unregisterServerCommand('wcs_change_race')