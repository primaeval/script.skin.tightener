import xbmc,xbmcaddon,xbmcvfs,xbmcgui
import re
import shutil


def log(x):
    xbmc.log(repr(x),xbmc.LOGERROR)
d = xbmcgui.Dialog()

def copyTree(src,dst,process=True):
    #log((src,dst))
    xbmcvfs.mkdirs(dst)
    dirs, files = xbmcvfs.listdir(src)
    for d in dirs:
        copyTree(src+d+'/',dst+d+'/',process)
    for f in files:
        ext = f.split('.')[-1]
        if process and ext in ['xml','txt','po']:
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

xml = xbmcvfs.File(old_path+'addon.xml','rb').read()
old_skin_name = re.search('<addon.*?name="(.*?)"',xml,flags=(re.DOTALL | re.MULTILINE)).group(1)
new_skin_name = d.input('New Skin Name (%s)' % old_skin_name, old_skin_name+' Fast')

if d.yesno('Skin Tightener','Make zip file'):
    new_path = 'special://temp/%s/%s/' % (new_skin,new_skin)
    if xbmcvfs.exists(new_path):
        ok = d.ok('Folder already exists', 'Overwrite %s ?' % new_path)
        if not ok:
            quit()

    #copyTree(old_path,new_path)
    #output_path ='special://temp/'+new_skin+'/'+new_skin+'/'
    output_top_path ='special://temp/'+new_skin+'/'
    output_zip = 'special://temp/'+new_skin
    copyTree(old_path,new_path)
    #copyTree(new_path,output_path,False)
    shutil.make_archive(xbmc.translatePath(output_zip), 'zip', xbmc.translatePath(output_top_path))
    xbmc.executebuiltin('ActivateWindow(AddonBrowser)')

quit()
new_path = 'special://home/addons/%s/' % new_skin
#new_path = 'special://temp/%s/%s/' % (new_skin,new_skin)
if xbmcvfs.exists(new_path):
    ok = d.ok('Folder already exists', 'Overwrite %s ?' % new_path)
    if not ok:
        quit()

xml = xbmcvfs.File(old_path+'addon.xml','rb').read()
old_skin_name = re.search('<addon.*?name="(.*?)"',xml,flags=(re.DOTALL | re.MULTILINE)).group(1)
new_skin_name = d.input('New Skin Name (%s)' % old_skin_name, old_skin_name+' Fast')
copyTree(old_path,new_path)
output_path ='special://temp/'+new_skin+'/'
output_zip = 'special://temp/'+new_skin

copyTree(new_path,output_path,False)
shutil.make_archive(xbmc.translatePath(output_zip), 'zip', xbmc.translatePath(output_path))
if d.yesno('Skin Tightener','Restart Kodi, Enable Skin in Addons\My Addons and Select "%s" as Skin in Settings\Interface or[CR]Press Yes to Add from zip file: [CR]%s.zip' % (new_skin_name,output_zip)):
    xbmc.executebuiltin('ActivateWindow(AddonBrowser)')
