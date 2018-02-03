import xbmc,xbmcaddon,xbmcvfs,xbmcgui
import re
import re, os, sys
import xbmc, xbmcgui, xbmcplugin, xbmcvfs, xbmcaddon
import time

if sys.version_info < (2, 7):
    import simplejson as json
else:
    import json


def log(x):
    xbmc.log(repr(x),xbmc.LOGERROR)

def copyTree(src,dst):
    #log((src,dst))
    xbmcvfs.mkdirs(dst)
    dirs, files = xbmcvfs.listdir(src)
    for d in dirs:
        copyTree(src+d+'/',dst+d+'/')
    for f in files:
        ext = f.split('.')[-1]
        if ext in ['xml','txt','po']:
            xml = xbmcvfs.File(src+f,'rb').read()
            if ext == 'xml':
                xml = re.sub('time=".*?"','time="0"',xml)
                xml = re.sub(r'(<scrolltime.*?>)(.*?)(</scrolltime>)',r'\g<1>0\g<3>',xml)
                xml = re.sub(r'(fadetime.*?>)(.*?)(</fadetime>)',r'\g<1>0\g<3>',xml)
            xml = re.sub(re.escape(old_skin),new_skin,xml)
            xml = re.sub(re.escape(old_skin_name),new_skin_name,xml)
            xbmcvfs.File(dst+f,'wb').write(xml)
        else:
            xbmcvfs.copy(src+f,dst+f)


d = xbmcgui.Dialog()

location = d.select("Choose Skin Location", ["System Skin", "Installed Skin"])
if location == -1:
    quit()
#TODO deal with current skin "special://skin/"
paths = ["special://xbmc/addons/", "special://home/addons/"]
path = paths[location]
old_path = d.browse(0, 'Choose Original Skin Folder', 'files', '', False, False, path)
if not old_path or old_path == path:
    quit()
old_skin = old_path.split('/')[-2]
new_skin = d.input("New Skin Folder (%s)" % old_skin, old_skin+'.fast')
if not new_skin:
    quit()
new_path = 'special://home/addons/%s/' % new_skin
if xbmcvfs.exists(new_path):
    ok = d.yesno('Folder already exists', 'Overwrite %s ?' % new_path)
    if not ok:
        quit()

xml = xbmcvfs.File(old_path+'addon.xml','rb').read()
old_skin_name = re.search('<addon.*?name="(.*?)"',xml,flags=(re.DOTALL | re.MULTILINE)).group(1)
new_skin_name = d.input('New Skin Name (%s)' % old_skin_name, old_skin_name+' Fast')
copyTree(old_path,new_path)

xbmc.executebuiltin("UpdateLocalAddons")
time.sleep(2)
params = '"method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}'% new_skin
try:
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", %s, "id": 1}' % params)
    xbmc.executebuiltin("ActivateWindow(appearancesettings)")
except:
    d.ok("Skin Tightener","Kodi web interface wasn't enabled. Restart Kodi and Enable Skin in My Addons.")








