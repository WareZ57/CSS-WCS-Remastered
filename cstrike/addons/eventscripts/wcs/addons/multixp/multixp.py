import es
import time

wcs_killxp1 = es.ServerVar('wcs_cfg_killxp')
wcs_knifexp1 = es.ServerVar('wcs_cfg_knifexp')
wcs_plantxp1 = es.ServerVar('wcs_cfg_plantxp')
wcs_explodexp1 = es.ServerVar('wcs_cfg_explodexp')
wcs_defusexp1 = es.ServerVar('wcs_cfg_defusexp')
wcs_headshotxp1 = es.ServerVar('wcs_cfg_headshotxp')
wcs_hostagexp1 = es.ServerVar('wcs_cfg_hostagexp')

#this defines at what rate xp should be highered. DON'T set this anything like 1.3252 but only 1, 2,3 and so on (no decimals!)
multiplicator = 2


tmp_killxp = wcs_killxp1*multiplicator
tmp_knifexp = wcs_knifexp1*multiplicator
tmp_plantxp = wcs_plantxp1*multiplicator
tmp_explodexp = wcs_explodexp1*multiplicator
tmp_defusexp = wcs_defusexp1*multiplicator
tmp_headshotxp = wcs_headshotxp1*multiplicator
tmp_hostagexp = wcs_headshotxp1*multiplicator

#The time double xp should start at
start = '14:20'

#The time dpuble xp should end add
end = '14:25'


#do not modify below if you don't know what you are doing
double_xp = 0


def load():
    if not es.exists("script", "crontab"): es.load("crontab")
    es.server.queuecmd('crontab %s %s * * * "es_xset double_xp 1' % ((start.split(':'))[1],(start.split(':'))[0]))
    es.server.queuecmd('crontab %s %s * * * "es_xset double_xp 0' % ((end.split(':'))[1],(end.split(':'))[0]))
    
    
def unload():
    es.set('wcs_cfg_killxp',wcs_killxp1)
    es.set('wcs_cfg_knifexp',wcs_knifexp1)
    es.set('wcs_cfg_plantxp',wcs_plantxp1)
    es.set('wcs_cfg_explodexp',wcs_explodexp1)
    es.set('wcs_cfg_defusexp',wcs_defusexp1)
    es.set('wcs_cfg_headshotxp',wcs_headshotxp1)
    es.set('wcs_cfg_hostagexp',wcs_hostagexp1)

    
def round_start(ev):
    double_xp = es.ServerVar('double_xp')
    if double_xp == 1:
        es.msg('#multi','#green[DoubleXP]#lightgreen is activated. Deactivating at #green%02s:%02s' % ((end.split(':'))[0],(end.split(':'))[1]))

        es.set('wcs_cfg_killxp',tmp_killxp)
        es.set('wcs_cfg_knifexp',tmp_knifexp)
        es.set('wcs_cfg_plantxp',tmp_plantxp)
        es.set('wcs_cfg_explodexp',tmp_explodexp)
        es.set('wcs_cfg_defusexp',tmp_defusexp)
        es.set('wcs_cfg_headshotxp',tmp_headshotxp)
        es.set('wcs_cfg_hostagexp',tmp_hostagexp)
        
    if double_xp != 1:
        es.msg('#multi','#green[DoubleXP]#lightgreen is deactivated. Activating at #green%02s:%02s' % ((start.split(':'))[0],(start.split(':'))[1]))
        es.set('wcs_cfg_killxp',wcs_killxp1)
        es.set('wcs_cfg_knifexp',wcs_knifexp1)
        es.set('wcs_cfg_plantxp',wcs_plantxp1)
        es.set('wcs_cfg_explodexp',wcs_explodexp1)
        es.set('wcs_cfg_defusexp',wcs_defusexp1)
        es.set('wcs_cfg_headshotxp',wcs_headshotxp1)
        es.set('wcs_cfg_hostagexp',wcs_hostagexp1)
