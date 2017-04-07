import xbmc,xbmcaddon,xbmcvfs,xbmcgui
import re

def log(x):
    xbmc.log(repr(x))
d = xbmcgui.Dialog()

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
            xml = re.sub(re.escape(old_skin),new_skin,xml) 
            xml = re.sub(re.escape(old_skin_name),new_skin_name,xml)
            xbmcvfs.File(dst+f,'wb').write(xml)
        else:
            xbmcvfs.copy(src+f,dst+f)
    

location = d.select("Choose Skin Location", ["System Skin", "Installed Skin"])
if location == -1:
    quit()
#TODO deal with current skin "special://skin/"
paths = ["special://xbmc/addons/", "special://home/addons/"]
path = paths[location]
old_path = d.browse(0, 'Choose Original Skin Folder', 'files', '', False, False, path)

old_skin = old_path.split('/')[-2]
new_skin = d.input("New Skin Folder (%s)" % old_skin, old_skin+'.fast')

new_path = 'special://home/addons/%s/' % new_skin
if xbmcvfs.exists(new_path):
    ok = d.ok('Folder already exists.', 'Overwrite? (%s)' % new_path)
    if not ok:
        quit()

xml = xbmcvfs.File(old_path+'addon.xml','rb').read()
old_skin_name = re.search('<addon.*?name="(.*?)"',xml,flags=(re.DOTALL | re.MULTILINE)).group(1)
new_skin_name = d.input('New Skin Name (%s)' % old_skin_name, old_skin_name+' Fast')
copyTree(old_path,new_path)
d.ok('Skin Tightener','Restart Kodi and Select %s as Skin' % new_skin_name)