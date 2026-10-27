##############################
#########CONFIG START#########
##############################

mysqlHost   = 'localhost'
mysqlUser   = 'root'
mysqlPasswd = ''
mysqlDB     = 'wcs_database'
mysqlSocket = '' # Leave mysqlSocket blank unless you know what your doing.

##############################
##########CONFIG END##########
##############################

##############################
##########DO NOT EDIT#########
########BELOW THIS LINE#######
#########OR BAD THINGS########
#########WILL HAPPEN!#########
##############################


import es
import socket

from wcs import wcs

import pymysql
from pymysql.exceptions import MySQLError



class MySQLManager(wcs.SQLiteManager):
	def __init__(self):
		pass

	def execute(self, statement, args=None, _tries=0):
		while isinstance(args, (list, tuple)) and len(args) == 1:
			args = args[0]

		try:
			self.cursor.execute(statement.replace('?','%s'), args)
		except socket.error:
			wcs.logging.log('mysql_connection: The connection to the MySQL database has been lost. Trying to reconnect...')

			_tries += 1

			if _tries == 5:
				wcs.logging.log('mysql_connection: Has been disabled (could not connect to remote database)')

				es.unload('wcs/addons/mysql_connection')
				return

			try:
				self.connect()
				self.execute(statement, args, _tries)
			except:
				self.execute(statement, args, _tries)
		except:
			self.cursor.execute(statement.replace('?',"'%s'"), args)

	def connect(self):
		if mysqlSocket:
			self.connection = pymysql.connect(host=str(mysqlHost), user=str(mysqlUser), passwd=str(mysqlPasswd), unix_socket=str(mysqlSocket))
		else:
			self.connection = pymysql.connect(host=str(mysqlHost), user=str(mysqlUser), passwd=str(mysqlPasswd))

		self.cursor     = self.connection.cursor()

		self.execute("CREATE DATABASE IF NOT EXISTS ?", str(mysqlDB))

		self.execute("USE ?", str(mysqlDB))

		self.execute("""\
			CREATE TABLE IF NOT EXISTS Players (
				UserID        INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
				steamid       VARCHAR(30) NOT NULL,
				currace       VARCHAR(30) NOT NULL,
				name          VARCHAR(30) NOT NULL,
				totallevel    INTEGER DEFAULT 0,
				lastconnect   INTEGER
			)""")

		self.execute("""\
			CREATE TABLE IF NOT EXISTS Races (
				RaceID        INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
				UserID        INTEGER NOT NULL,
				name          VARCHAR(50) NOT NULL,
				skills        VARCHAR(50) NOT NULL,
				level         INTEGER DEFAULT 0,
				xp            INTEGER DEFAULT 0,
				unused        INTEGER DEFAULT 0
			)""")

	def save(self):
		self.connection.commit()

	def close(self):
		self.cursor.close()
		self.connection.close()
newDatabase = MySQLManager()

def player_disconnect(ev):
	newDatabase.save()

def load():
	for x in wcs.tmp:
		wcs.tmp[x].save()

	wcs.tmp.clear()

	wcs.database.save()
	wcs.database.close()

	try:
		newDatabase.connect()
	except MySQLError, e:
		wcs.logging.log('mysql_connection: Could not connect to database. Error: '+str(e))
		raise MySQLError, e

	wcs.database = newDatabase

def unload():
	for x in wcs.tmp:
		wcs.tmp[x].save()

	wcs.tmp.clear()

	try:
		newDatabase.save()
		newDatabase.close()
	except:
		pass

	wcs.database = wcs.SQLiteManager(wcs.Path(wcs.ini.path).joinpath('data'))