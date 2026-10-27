import es
import cmdlib
import playerlib
from wcs import wcs


def load():
	cmdlib.registerServerCommand('wcs_item_give', _item_give, 'wcs_item_give <userid> <item>')


def _item_give(args):
	userid = int(args[0])
	item = str(args[1])
	player = playerlib.getPlayer(userid)
	iteminfo = wcs.itemdb.getItem(item)
	wcs.shopmenu.addItem(userid, item)
	es.tell(userid, '#multi', '#greenAdmin gave you #lightgreen '+str(item))
	cash = player.getCash()
	player.setCash(cash + int(iteminfo['cost']))


def unload():
	cmdlib.unregisterServerCommand('wcs_item_give')