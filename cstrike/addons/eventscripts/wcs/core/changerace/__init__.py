import es
from popuplib import create, send
import playerlib
import wcs
listofargs = {}
popups = []
		
def HowChange(userid, args=0):
	if args:
		if wcs.wcs.changerace_racename:
			racename(userid, args)
		elif wcs.wcs.racecategories:
			raceCategories(userid)
			es.msg(str(wcs.wcs.racecategories))

		else:
			doCommand(userid, 'changerace')
	else:
		if wcs.wcs.racecategories:
			raceCategories(userid)
			es.msg(str(wcs.wcs.racecategories))

		else:
			doCommand(userid, 'changerace')
		
def racename(userid, args):
	if userid in listofargs:
		listofargs[userid].append(str(args))
	else:
		listofargs[userid] = []
		listofargs[userid].append(str(args))
	v = availableraces(userid)
	if v:
		Changerace_racename(userid)
	else:
		wcs.wcs.tell(userid, 'changerace_racename: no races')
 
def doCommand(userid, args='changerace', msg=True):
   if es.exists('userid', userid):
      if args == 'changerace':
         args = 'changerace7'
 
      positionsearch = str(args.replace('changerace', '').strip())
 
      if len(positionsearch):
         if positionsearch.isdigit():
            positionsearch = int(positionsearch)
         else:
            positionsearch = 7
      else:
         positionsearch = 7
 
      races = wcs.wcs.racedb.getAll()
 
      #allraces = sorted(races, key=lambda x: races[x]['required'], reverse=False)
      allraces = races.keys()
 
      del allraces[:positionsearch - 7]
      del allraces[positionsearch:]
 
      if len(allraces):
         pname = 'changerace_%s_%s'%(userid, positionsearch)
         popups.append(pname)
         changerace = create(pname)
 
         changerace.addline('Please choose a race')
 
         changerace.addline(' ')
         changerace.menuselect = callBack
 
         player = wcs.wcs.getPlayer(userid)
 
         totallevel = player.player.totallevel
 
         added = 0
         for number, race in enumerate(allraces):
            if number < 7:
               added += 1
               v = canUse(userid, race)
               raceinfo = wcs.wcs.racedb.getRace(race)
               team = es.getplayerteam(userid)
               if not v:
                  if wcs.wcs.showracelevel:
                     level = wcs.wcs._getRace(player.player.UserID, race, userid).level
                  else:
                     level = 0
                  changerace.addline('->'+str(number+1)+'. '+str(race)+(' - Current level: '+str(level) if level else ''))
               elif v == 1:
                  if team in (2,3):
                     team = {2:'T',3:'CT'}[team]
 
                     changerace.addline(str(number+1)+'. '+str(race)+' (teamlimit '+raceinfo['teamlimit']+')')
                     changerace.submenu(number+1, pname)
                  else:
                     if wcs.wcs.showracelevel:
                        level = wcs.wcs._getRace(player.player.UserID, race, userid).level
                     else:
                        level = 0
                     changerace.addline('->'+str(number+1)+'. '+str(race)+(' - Current level: '+str(level) if level else ''))
                  '''if wcs.wcs.showracelevel:
                     level = wcs.wcs._getRace(player.player.UserID, race, userid).level
                  else:
                     level = 0
                  changerace.addline('->'+str(number+1)+'. '+str(race)+(' - Current level: '+str(level) if level else ''))'''
               elif v == 2:
                  changerace.addline(str(number+1)+'. '+str(race)+' (maximum level '+str(raceinfo['maximum'])+')')
                  changerace.submenu(number+1, pname)
               elif v == 3:
                  changerace.addline(str(number+1)+'. '+str(race)+' (minimum level '+raceinfo['required']+')')
                  changerace.submenu(number+1, pname)
               elif v == 4:
                  if team in (2,3):
                     changerace.addline(str(number+1)+'. '+str(race)+' (restricted team '+{2:'T',3:'CT'}[team]+')')
                     changerace.submenu(number+1, pname)
                  else:
                     if wcs.wcs.showracelevel:
                        level = wcs.wcs._getRace(player.player.UserID, race, userid).level
                     else:
                        level = 0
                     changerace.addline('->'+str(number+1)+'. '+str(race)+(' - Current level: '+str(level) if level else ''))
               elif v == 5:
                  changerace.addline(str(number+1)+'. '+str(race)+' (private race)')
                  changerace.submenu(number+1, pname)
               elif v == 6:
                  changerace.addline(str(number+1)+'. '+str(race)+' (restricted map '+wcs.wcs.curmap+')')
                  changerace.submenu(number+1, pname)
               '''raceinfo = wcs.wcs.racedb.getRace(race)
 
               if not wcs.wcs.curmap in raceinfo['restrictmap'].split('|'):
                  admins = raceinfo['allowonly'].split('|')
                  if len(admins) == 1 and not admins[0]:
                     del admins[0]
 
                  if not len(admins) or len(admins) and (es.getplayersteamid(userid) in admins or 'ADMINS' in admins) and es.getplayersteamid(userid) in wcs.wcs.admin.admins:
                     team = int(es.getplayerteam(userid))
                     if not raceinfo['restrictteam'] or not int(raceinfo['restrictteam']) == team:
                        if totallevel >= int(raceinfo['required']):
                           if int(raceinfo['maximum']) and totallevel <= int(raceinfo['maximum']):
                              changerace.addline(''+str(number+1)+'. '+str(race)+' (maximum level '+str(raceinfo['maximum'])+')')
                              changerace.submenu(number+1, pname)
                           else:
                              changerace.addline('->'+str(number+1)+'. '+str(race))
                        else:
                           changerace.addline(''+str(number+1)+'. '+str(race)+' (minimum level '+raceinfo['required']+')')
                           changerace.submenu(number+1, pname)
                     else:
                        changerace.addline(''+str(number+1)+'. '+str(race)+' (restricted team '+{2:'T',3:'CT'}[team]+')')
                        changerace.submenu(number+1, pname)
                  else:
                     changerace.addline(''+str(number+1)+'. '+str(race)+' (private race)')
                     changerace.submenu(number+1, pname)
               else:
                  changerace.addline(''+str(number+1)+'. '+str(race)+' (restricted map '+wcs.wcs.curmap+')')
                  changerace.submenu(number+1, pname)'''
            else:
               break
 
         while added < 7:
            changerace.addline(' ')
            added += 1
            changerace.submenu(added, pname)
 
         changerace.addline(' ')
         if positionsearch < 8:
            changerace.addline(' ')
            changerace.submenu(8, pname)
         else:
            changerace.addline('->8. Back')
 
         if len(races.keys()) < positionsearch+1:
            changerace.addline(' ')
            changerace.submenu(9, pname)
         else:
            changerace.addline('->9. Next')
 
         changerace.addline('0. Close')
 
         if positionsearch == 7:
            if msg:
               wcs.wcs.tell(userid, 'changerace: still alive')
 
         changerace.send(userid)
         es.ServerVar('wcs_ppuser').set(userid)
         es.doblock("wcs/tools/pending/pending")
 
 
def popupHandler(userid, choice, popupid):
   if es.exists('userid', userid):
      last_split  = popupid.split('_')
      last_search = int(last_split[2])
 
      races = wcs.wcs.racedb.getAll()
 
      if choice == 8:
         if last_search < 0:
            doCommand(userid, 'changerace7')
 
         elif last_search < 6:
            send(popupid, userid)
 
         else:
            newsearch = int(last_search)-7
            doCommand(userid, 'changerace%s'%newsearch, False)
 
      elif choice == 9:
         #if last_search >= len(races.keys()):
         #   send(popupid, userid)
 
         #else:
         if last_search < len(races.keys()):
            newsearch = int(last_search)+7
            doCommand(userid, 'changerace%s'%newsearch, False)
 
      elif choice < 8:
         race_select = choice-1
         #race_select = divmod(last_search, 7)[0]*7-(8-choice) #Find the number where the race is placed
 
         #allraces = sorted(races, key=lambda x: races[x]['required'], reverse=False)
         allraces = races.keys()
 
         del allraces[:last_search - 7]
         del allraces[last_search:]
 
         try:
            player = wcs.wcs.getPlayer(userid)
            totallevel = player.player.totallevel
 
            race = allraces[race_select]
            raceinfo = wcs.wcs.racedb.getRace(race)
            team = int(es.getplayerteam(userid))
            teamlimit = raceinfo['teamlimit']
            admins = raceinfo['allowonly'].split('|')
         
            if len(admins) == 1 and not admins[0]:
               del admins[0]
 
            if wcs.wcs.curmap in raceinfo['restrictmap'].split('|'):
               wcs.wcs.tell(userid, 'changerace: restricted map', {'race':race, 'map':wcs.wcs.curmap})
 
            #elif len(admins) and (es.getplayersteamid(userid) not in admins or 'ADMINS' in admins) and not es.getplayersteamid(userid) in wcs.wcs.admin.admins:
	    elif len(admins) and (es.getplayersteamid(userid) not in admins or ('ADMINS' in admins and es.getplayersteamid(userid) not in admins)) and (es.getplayersteamid(userid) not in wcs.wcs.admin.admins):
               wcs.wcs.tell(userid, 'changerace: restricted player', {'race':race})
 
            elif int(raceinfo['restrictteam']) and int(raceinfo['restrictteam']) == team:
               wcs.wcs.tell(userid, 'changerace: restricted team', {'race':race, 'team':{2:'T',3:'CT'}[team]})
 
            elif totallevel < int(raceinfo['required']):
               diffience = str(int(raceinfo['required'])-int(player.player.totallevel))
               wcs.wcs.tell(userid, 'changerace: required level', {'race':race, 'diffience':diffience})
 
            elif int(raceinfo['maximum']) and totallevel > int(raceinfo['maximum']):
               diffience = str(int(player.player.totallevel)-int(raceinfo['maximum']))
               wcs.wcs.tell(userid, 'changerace: high level', {'race':race, 'diffience':diffience})
 
            elif team in (2,3) and 'teamlimit' in raceinfo and len(filter(lambda x: race == wcs.wcs.getPlayer(x).race.name, filter(lambda x: es.getplayerteam(x) == es.getplayerteam(userid), es.getUseridList()))) >= int(raceinfo['teamlimit']) and not int(raceinfo['teamlimit']) == 0:
               wcs.wcs.tell(userid, 'changerace: team limit', {'race':race, 'teamlimit' :teamlimit})
 
            else:
               if es.ServerVar("wcs_changerace_mode") == 1:
                  wcs.wcs.tell(userid, 'changerace: change race', {'race':race})
                  player.changeRace(race)
  
                  wcs.wcs.wcsgroup.setUser(userid, 'ability', 0)
  
               elif es.ServerVar("wcs_changerace_mode") == 2:
                  wcs.wcs.tell(userid, 'changerace: change round', {'race':race})
                  wcs.wcs.wcsgroup.setUser(userid, 'changerace', race)
                  
                  wcs.wcs.wcsgroup.setUser(userid, 'ability', 0)
 
               #keydelete('WCSuserdata', userid)
               #keycreate('WCSuserdata', userid)
               #wcs.wcs.wcsgroup.delUser(userid)
               #wcs.wcs.wcsgroup.addUser(userid)
         except IndexError:
            pass
			
def raceCategories(userid, args='racecats', msg=True):
	if es.exists('userid', userid):
		
		if args == 'racecats':
			args = 'racecats7'
			
		positionsearch = str(args.replace('racecats', '').strip())
		if len(positionsearch):
			if positionsearch.isdigit():
				positionsearch = int(positionsearch)
			else:
				positionsearch = 7
		else:
			positionsearch = 7
		#races = availableraces(userid)
		races = wcs.wcs.racecats.getCategories()
		del races[:positionsearch - 7]
		del races[positionsearch:]
 
		if len(races):
			pname = 'racecats_%s_%s'%(userid, positionsearch)
			popups.append(pname)
			racecats = create(pname)
			racecats.addline('Please choose races category')
 
			racecats.addline(' ')
			racecats.menuselect = selecter
 
			added = 0
			for number, race in enumerate(races):
				if number < 7:
					added += 1
					racecats.addline('->'+str(number+1)+'. '+str(race))
				else:
					break
 
			while added < 7:
				racecats.addline(' ')
				added += 1
				racecats.submenu(added, pname)
 
			racecats.addline(' ')
			if positionsearch < 8:
				racecats.addline(' ')
				racecats.submenu(8, pname)
			else:
				racecats.addline('->8. Back')
			
			if len(wcs.wcs.racecats.getCategories()) < positionsearch+1:
				racecats.addline(' ')
				racecats.submenu(9, pname)
			else:
				racecats.addline('->9. Next')
 
			racecats.addline('0. Close')
 
 
			racecats.send(userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")
			
def selecter(userid, choice, popupid):
	if es.exists('userid', userid):
		last_split  = popupid.split('_')
		last_search = int(last_split[2])
 
 
		if choice == 8:
			if last_search < 0:
				raceCategories(userid, 'racecats7')
 
			elif last_search < 6:
				send(popupid, userid)
 
			else:
				newsearch = int(last_search)-7
				raceCategories(userid, 'racecats%s'%newsearch, False)
 
		elif choice == 9:
			if last_search < len(wcs.wcs.racecats.getCategories()):
				newsearch = int(last_search)+7
				raceCategories(userid, 'racecats%s'%newsearch, False)
 
		elif choice < 8:
			allraces = wcs.wcs.racecats.getCategories()
			del allraces[:last_search - 7]
			del allraces[last_search:]
			cat_select = choice-1
			v = wcs.wcs.racecats.getRacesInCategories(cat_select)
			if v:
				raceCategories1(userid, 'raceselect_%s_%s_%s'%(userid,7,choice-1))
			else:
				wcs.wcs.tell(userid, 'racecategories: no races')
				raceCategories(userid, 'racecats%s'%last_search, False)
				
				
def raceCategories1(userid, args, msg=True):
	if es.exists('userid', userid):
		if args == 'raceselect':
			args = 'raceselect7'
		positionsearch = args.split('_')[2]
		catnumber = int(args.replace('raceselect', '').strip().split('_')[3])
		
		#category = wcs.racecats.getRacesInCategories(int(args.replace('raceselect', '').strip().split('_')[1]))
		if len(positionsearch):
			if positionsearch.isdigit():
				positionsearch = int(positionsearch)
			else:
				positionsearch = 7
		else:
			positionsearch = 7
		
		#races = availableraces(userid)
		races = wcs.wcs.racecats.getRacesInCategories(catnumber)
		del races[:positionsearch - 7]
		del races[positionsearch:]
		
		if len(races):
			pname = 'raceselect_%s_%s_%s'%(userid, positionsearch,catnumber)
			popups.append(pname)
			raceselect = create(pname)
			raceselect.addline('Please choose races')
			player = wcs.wcs.getPlayer(userid)
			raceselect.addline(' ')
			raceselect.menuselect = selecter1
			
			added = 0
			for number, race in enumerate(races):
				if number < 7:
					added += 1
					
					v = canUse(userid, race)
					
					raceinfo = wcs.wcs.racedb.getRace(race)
					
					team = es.getplayerteam(userid)
					
					if not v:
						if wcs.wcs.showracelevel:
							level = wcs.wcs._getRace(player.player.UserID, race, userid).level
						else:
							level = 0
						raceselect.addline('->'+str(number+1)+'. '+str(race)+(' - Current level: '+str(level) if level else ''))
					elif v == 1:
						if team in (2,3):
							team = {2:'T',3:'CT'}[team]
 
							raceselect.addline(str(number+1)+'. '+str(race)+' (teamlimit '+raceinfo['teamlimit']+')')
							raceselect.submenu(number+1, pname)
						else:
							if wcs.wcs.showracelevel:
								level = wcs.wcs._getRace(player.player.UserID, race, userid).level
							else:
								level = 0
							raceselect.addline('->'+str(number+1)+'. '+str(race)+(' - Current level: '+str(level) if level else ''))
					elif v == 2:
						raceselect.addline(str(number+1)+'. '+str(race)+' (maximum level '+str(raceinfo['maximum'])+')')
						raceselect.submenu(number+1, pname)
					elif v == 3:
						raceselect.addline(str(number+1)+'. '+str(race)+' (minimum level '+raceinfo['required']+')')
						raceselect.submenu(number+1, pname)
					elif v == 4:
						if team in (2,3):
							raceselect.addline(str(number+1)+'. '+str(race)+' (restricted team '+{2:'T',3:'CT'}[team]+')')
							raceselect.submenu(number+1, pname)
						else:
							if wcs.wcs.showracelevel:
								level = wcs.wcs._getRace(player.player.UserID, race, userid).level
							else:
								level = 0
							raceselect.addline('->'+str(number+1)+'. '+str(race)+(' - Current level: '+str(level) if level else ''))
					elif v == 5:
						raceselect.addline(str(number+1)+'. '+str(race)+' (private race)')
						raceselect.submenu(number+1, pname)
					elif v == 6:
						raceselect.addline(str(number+1)+'. '+str(race)+' (restricted map '+wcs.wcs.curmap+')')
						raceselect.submenu(number+1, pname)
				else:
					break
 
			while added < 7:
				raceselect.addline(' ')
				added += 1
				raceselect.submenu(added, pname)
 
			raceselect.addline(' ')
			if positionsearch < 8:
				raceselect.addline('->8. Back')
				#raceselect.addline(' ')
				#raceselect.submenu(8, pname)
			else:
				raceselect.addline('->8. Back')
			if len(wcs.wcs.racecats.getRacesInCategories(catnumber)) < positionsearch+1:
				raceselect.addline(' ')
				raceselect.submenu(9, pname)
			else:
				raceselect.addline('->9. Next')
 
			raceselect.addline('0. Close')
 
			if positionsearch == 7:
				if msg:
					wcs.wcs.tell(userid, 'changerace: still alive')
 
			raceselect.send(userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")
			
def selecter1(userid, choice, popupid):
	if es.exists('userid', userid):
		last_split  = popupid.split('_')
		last_search = int(last_split[2])
 
 
		if choice == 8:
			if last_search < 0:
				raceCategories1(userid, 'raceselect_%s_%s_%s'%(last_split[1],last_split[2],last_split[3]))
 
			elif last_search == 7:
				#send(popupid, userid)
				raceCategories(userid, 'racecats', False)
 
			else:
				newsearch = int(last_search)-7
				raceCategories1(userid, 'raceselect_%s_%s_%s'%(last_split[1],newsearch,last_split[3]), False)
 
		elif choice == 9:
			if last_search < len(wcs.wcs.racecats.getRacesInCategories(int(last_split[3]))):
				newsearch = int(last_search)+7
				raceCategories1(userid, 'raceselect_%s_%s_%s'%(last_split[1],newsearch,last_split[3]), False)
 
		elif choice < 8:
			race_select = choice-1
			allraces = wcs.wcs.racecats.getRacesInCategories(int(last_split[3]))
			del allraces[:last_search - 7]
			del allraces[last_search:]
 
        try:
			player = wcs.wcs.getPlayer(userid)
			totallevel = player.player.totallevel
 
			race = allraces[race_select]
			raceinfo = wcs.wcs.racedb.getRace(race)
			team = int(es.getplayerteam(userid))
			teamlimit = raceinfo['teamlimit']
			admins = raceinfo['allowonly'].split('|')
         
			if len(admins) == 1 and not admins[0]:
				del admins[0]
 
			if wcs.wcs.curmap in raceinfo['restrictmap'].split('|'):
				wcs.wcs.tell(userid, 'changerace: restricted map', {'race':race, 'map':wcs.wcs.curmap})
 
            #elif len(admins) and (es.getplayersteamid(userid) not in admins or 'ADMINS' in admins) and not es.getplayersteamid(userid) in wcs.wcs.admin.admins:
			elif len(admins) and (es.getplayersteamid(userid) not in admins or ('ADMINS' in admins and es.getplayersteamid(userid) not in admins)) and (es.getplayersteamid(userid) not in wcs.wcs.admin.admins):
				wcs.wcs.tell(userid, 'changerace: restricted player', {'race':race})
 
			elif int(raceinfo['restrictteam']) and int(raceinfo['restrictteam']) == team:
				wcs.wcs.tell(userid, 'changerace: restricted team', {'race':race, 'team':{2:'T',3:'CT'}[team]})
 
			elif totallevel < int(raceinfo['required']):
				diffience = str(int(raceinfo['required'])-int(player.player.totallevel))
				wcs.wcs.tell(userid, 'changerace: required level', {'race':race, 'diffience':diffience})
 
			elif int(raceinfo['maximum']) and totallevel > int(raceinfo['maximum']):
				diffience = str(int(player.player.totallevel)-int(raceinfo['maximum']))
				wcs.wcs.tell(userid, 'changerace: high level', {'race':race, 'diffience':diffience})
 
			elif team in (2,3) and 'teamlimit' in raceinfo and len(filter(lambda x: race == wcs.wcs.getPlayer(x).race.name, filter(lambda x: es.getplayerteam(x) == es.getplayerteam(userid), es.getUseridList()))) >= int(raceinfo['teamlimit']) and not int(raceinfo['teamlimit']) == 0:
				wcs.wcs.tell(userid, 'changerace: team limit', {'race':race, 'teamlimit' :teamlimit})
 
			else:
				if es.ServerVar("wcs_changerace_mode") == 1:
					wcs.wcs.tell(userid, 'changerace: change race', {'race':race})
					player.changeRace(race)
  
					wcs.wcs.wcsgroup.setUser(userid, 'ability', 0)
  
				if es.ServerVar("wcs_changerace_mode") == 2:
					wcs.wcs.tell(userid, 'changerace: change round', {'race':race})
					wcs.wcs.wcsgroup.setUser(userid, 'changerace', race)
                  
					wcs.wcs.wcsgroup.setUser(userid, 'ability', 0)
 
               #keydelete('WCSuserdata', userid)
               #keycreate('WCSuserdata', userid)
               #wcs.wcs.wcsgroup.delUser(userid)
               #wcs.wcs.wcsgroup.addUser(userid)
        except IndexError:
            pass
 
def canUse(userid, race):
   raceinfo = wcs.wcs.racedb.getRace(race)
 
   if not wcs.wcs.curmap in raceinfo['restrictmap'].split('|'):
      admins = raceinfo['allowonly'].split('|')
      #if len(admins) == 1 and not admins[0]:
      #   del admins[0]
 
      #if len(admins) and (es.getplayersteamid(userid) not in admins or 'ADMINS' in admins) and not es.getplayersteamid(userid) in wcs.wcs.admin.admins
      #if not len(admins) or len(admins) and (es.getplayersteamid(userid) in admins or 'ADMINS' in admins) and es.getplayersteamid(userid) in wcs.wcs.admin.admins:
      if (len(admins) and not admins[0]) or (es.getplayersteamid(userid) in admins) or ('ADMINS' in admins and es.getplayersteamid(userid) in wcs.wcs.admin.admins):
         team = int(es.getplayerteam(userid))
         if not raceinfo['restrictteam'] or not int(raceinfo['restrictteam']) == team:
            totallevel = wcs.wcs.getPlayer(userid).player.totallevel
            if totallevel >= int(raceinfo['required']):
               if int(raceinfo['maximum']) and totallevel > int(raceinfo['maximum']):
                  return 2
               else:
                  if team in (2,3) and len(filter(lambda x: race == wcs.wcs.getPlayer(x).race.name, filter(lambda x: es.getplayerteam(x) == es.getplayerteam(userid), es.getUseridList()))) >= int(raceinfo['teamlimit']) and not int(raceinfo['teamlimit']) == 0:
                     return 1
 
                  return 0
            return 3
         return 4
      return 5
   return 6
 
 
callBack = popupHandler


def Changerace_racename(userid, args='racename', msg=True):
	if es.exists('userid', userid):
		
		if args == 'racename':
			args = 'racename7'
		positionsearch = str(args.replace('racename', '').strip())
		if len(positionsearch):
			if positionsearch.isdigit():
				positionsearch = int(positionsearch)
			else:
				positionsearch = 7
		else:
			positionsearch = 7
		#races = availableraces(userid)
		races = availableraces(userid)
		del races[:positionsearch - 7]
		del races[positionsearch:]
 
		if len(races):
			pname = 'racename_%s_%s'%(userid, positionsearch)
			popups.append(pname)
			racename = create(pname)
			racename.addline('Please choose a race')
			racename.addline(' ')
			racename.menuselect = selecter2
			player = wcs.wcs.getPlayer(userid)
 
			#totallevel = player.player.totallevel
			added = 0
			for number, race in enumerate(races):
				if number < 7:
					added += 1
					if wcs.wcs.showracelevel:
						level = wcs.wcs._getRace(player.player.UserID, race, userid).level
					else:
						level = 0
					racename.addline('->'+str(number+1)+'. '+str(race)+(' - Current level: '+str(level) if level else ''))
				else:
					break
			while added < 7:
				racename.addline(' ')
				added += 1
				racename.submenu(added, pname)
			racename.addline(' ')
			if positionsearch < 8:
				racename.addline(' ')
				racename.submenu(8, pname)
			else:
				racename.addline('->8. Back')
			if len(availableraces(userid)) < positionsearch+1:
				racename.addline(' ')
				racename.submenu(9, pname)
			else:
				racename.addline('->9. Next')
 
			racename.addline('0. Close')
 
			if positionsearch == 7:
				if msg:
					wcs.wcs.tell(userid, 'changerace: still alive')
 
			racename.send(userid)
			es.ServerVar('wcs_ppuser').set(userid)
			es.doblock("wcs/tools/pending/pending")


def selecter2(userid, choice, popupid):
	if es.exists('userid', userid):
		last_split  = popupid.split('_')
		last_search = int(last_split[2])
 
		races = listofargs[userid]
 
		if choice == 8:
			if last_search < 0:
				Changerace_racename(userid, 'racename7')
 
			elif last_search < 6:
				send(popupid, userid)
 
			else:
				newsearch = int(last_search)-7
				Changerace_racename(userid, 'racename%s'%newsearch, False)
 
		elif choice == 9:
			if last_search < len(availableraces(userid)):
				newsearch = int(last_search)+7
				Changerace_racename(userid, 'racename%s'%newsearch, False)
 
		elif choice < 8:
			race_select = choice-1
			allraces = availableraces(userid)
			del allraces[:last_search - 7]
			del allraces[last_search:]
 
			try:
				player = wcs.wcs.getPlayer(userid)
				totallevel = player.player.totallevel
 
				race = allraces[race_select]
				player.changeRace(race)
  
				wcs.wcs.wcsgroup.setUser(userid, 'ability', 0)
  
				if es.ServerVar("wcs_changerace_mode") == 1:
					wcs.wcs.tell(userid, 'changerace: change race', {'race':race})
					player.changeRace(race)
  
					wcs.wcs.wcsgroup.setUser(userid, 'ability', 0)

				if es.ServerVar("wcs_changerace_mode") == 2:
					wcs.wcs.tell(userid, 'changerace: change round', {'race':race})
					wcs.wcs.wcsgroup.setUser(userid, 'changerace', race)
                  
					wcs.wcs.wcsgroup.setUser(userid, 'ability', 0)
 
			except IndexError:
				pass 
			
def availableraces(userid):
	races = []
	allraces = wcs.wcs.racedb.getAll().keys()
	args = listofargs[userid][len(listofargs[userid])-1]
	for race in allraces:
		v = canUse(userid, race)
		if not v:
			if str(args) in str(race):
				races.append(race)
	if len(races):
		return races
	return None
		

def getPopups():
   return popups