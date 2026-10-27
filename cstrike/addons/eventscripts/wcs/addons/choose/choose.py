import es
import cmdlib
import time
import gamethread
from random import choice
from wcs.wcs import logging, getPlayer, racedb

races = racedb.getAll().keys()


racetime = "00:00"


def load():
	randrace = choice(races)
	es.ServerVar('wcs_rotdrace').set(randrace)
	gamethread.delayed(10, check)
  
#check()



def check():
	if time.strftime("%d:%m") == racetime:
		randrace = choice(races)
		es.ServerVar('wcs_rotdrace').set(randrace)
		gamethread.delayed(10, check)
