import es
import playerlib
from wcs import wcs

#Enable or disable VIP features here.
vip_addhealth = 2 #0 = disabled, 1 = on spawn, 2 =  on kill
vip_addarmor = 2 #0 = disabled, 1 = on spawn, 2 =  on kill
vip_addcash = 2 #0 = disabled, 1 = on spawn, 2 =  on kill
vip_message = 1 #0 = no messages, 1 = messages


#Feature Config
vip_health = 10
vip_armor = 30
vip_cash = 1000
vip_xp = 0.5 #0.1 = 10% 0.2 = 20% 0.3 = 30% and so on
vip_spawnxp = 10 



killxp = es.ServerVar('wcs_cfg_killxp')

def player_spawn(event_var):
	userid = event_var['userid']
	player = playerlib.getPlayer(userid)
	admin = wcs.admin.getPlayer(userid)
	if admin.hasFlag('vip'):
		if admin.hasFlag('vip_addhealth') and vip_addhealth == 1:
			player.setHealth(100+vip_health)
			if vip_message == 1:
				es.tell(userid, "#multi", "#green[WCS-VIP] #defaultYou got #green%s #defaultextra Health!" % (vip_health))
		if admin.hasFlag('vip_addarmor') and vip_addarmor == 1:
			armor = player.getArmor()
			player.setArmor(vip_armor+armor)
			if vip_message == 1:
				es.tell(userid, "#multi", "#green[WCS-VIP] #defaultYou got #green%s #defaultextra Health!" % (vip_armor))
		if admin.hasFlag('vip_addcash') and vip_addcash == 1:
			cash = player.getCash()
			player.setCash(vip_cash+cash)
			if vip_message == 1:
				es.tell(userid, "#multi", "#green[WCS-VIP] #defaultYou got #green%s #defaultextra Cash!" % (vip_cash))
		if admin.hasFlag('vip_addxp') and vip_spawnxp == 1:
			wcs.getPlayer(userid).giveXp(vip_spawnxp)
			if vip_message == 1:
				es.tell(userid, "#multi", "#green[WCS-VIP] #defaultYou got #green%s #defaultextra XP!" % (vip_spawnxp))
	



def player_death(event_var):
	userid = event_var['attacker']
	player = playerlib.getPlayer(userid)
	admin = wcs.admin.getPlayer(userid)
	if admin.hasFlag('vip_addxp') and vip_addxp == 2:
		wcs.getPlayer(userid).giveXp(round(killxp*vip_xp))
		if vip_message == 1:
			es.tell(userid, "#multi", "#green[WCS-VIP] #defaultYou got #green%s #defaultextra XP for killing an enemy!" % (round(killxp*vip_xp)))			
	if admin.hasFlag('vip_addhealth') and vip_addhealth == 2:
		health = player.getHealth()
		player.setHealth(player.getHealth()+vip_health)
		if vip_message == 1:
			es.tell(userid, "#multi", "#green[WCS-VIP] #defaultYou got #green%s #defaultextra Health for killing an enemy!" % (vip_health))
	if admin.hasFlag('vip_addarmor') and vip_addarmor == 2:
		armor = player.getArmor()
		player.setArmor(vip_armor+armor)
		if vip_message == 1:
			es.tell(userid, "#multi", "#green[WCS-VIP] #defaultYou got #green%s #defaultextra Armor for killing an enemy!" % (vip_armor))
	if admin.hasFlag('vip_addcash') and vip_addcash == 2:
		cash = player.getCash()
		player.setCash(vip_cash+cash)
		if vip_message == 1:
			es.tell(userid, "#multi", "#green[WCS-VIP] #defaultYou got #green%s #defaultextra Cash for killing an enemy!" % (vip_armor))
		

			


			
			
			
	
	