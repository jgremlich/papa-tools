import os, glob, time
import shutil
from ConfigParser import ConfigParser

def _writeConfigFile(filePath, configParser):
    """
    Will update the config file specified by filePath with the contents of configParser
    @precondition: filePath is a valid path
    @precondition: confgParser is an instance of ConfigParser()
    """
    configFile = open(filePath, 'wb')
    configParser.write(configFile)
       
def getUsername():
    return os.environ['USER']

def createNodeInfoFile(dirPath, toKeep):
    """
    Creates the .nodeInfo file in the directory specified by dirPath.
    The Node:Type must be set by concrete nodes
    @precondition: dirPath is a valid directory
    @postcondition: All sections/tags are created and set except "Type".
        "Type" must be set by concrete nodes.
    """
    username = getUsername()
    timestamp = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime())
    
    nodeInfo = ConfigParser()
    nodeInfo.add_section('Node')
    nodeInfo.set('Node', 'Type', '')
    
    nodeInfo.add_section('Versioning')
    nodeInfo.set('Versioning', 'LatestVersion', '0')
    nodeInfo.set('Versioning', 'VersionsToKeep', str(toKeep))
    nodeInfo.set('Versioning', 'Locked', 'False')
    nodeInfo.set('Versioning', 'LastCheckoutTime', timestamp)
    nodeInfo.set('Versioning', 'LastCheckoutUser', username)
    nodeInfo.set('Versioning', 'LastCheckinTime', timestamp)
    nodeInfo.set('Versioning', 'LastCheckinUser', username)
    nodeInfo.add_section('Comments')
    nodeInfo.set('Comments', 'v000', 'New')

    _writeConfigFile(os.path.join(dirPath, ".nodeInfo"), nodeInfo)

def addProjectFolder(parent, name):
    newPath = os.path.join(parent, name)
    os.makedirs(newPath)
    return newPath

def addVersionedFolder(parent, name, toKeep):
    new_dir = os.path.join(parent, name)
    os.makedirs(os.path.join(new_dir, "src", "v000"))
    os.makedirs(os.path.join(new_dir, "stable"))
    os.makedirs(os.path.join(new_dir, 'stable', 'backups'))

    #os.symlink(os.path.join(new_dir, 'stable', getNullReference()), os.path.join(new_dir, 'stable','stable'))
    #TODO change for stable selection
    #os.symlink(getNullReference(), os.path.join(new_dir, 'stable','stable'))
    createNodeInfoFile(new_dir, toKeep)
    return new_dir
    
def copyTemplateAnimation(self, shotName):
    template = os.path.join(os.environ['SHOTS_DIR'], 'static/animation/stable/static_animation_stable.mb')
    if(os.path.exists(template)):
        dest = os.path.join(shotName, 'animation/src/v000/'+shotName+'_animation.mb')
        shutil.copyfile(template, dest)
        print 'copied '+template+' to '+dest
    return

def createNewShotFolders(name):
    if(name == 'Model' or name == 'Rig'):
        parent = os.environ['ASSETS_DIR']
    if(name == 'Animation'):
        parent = os.environ['SHOTS_DIR']
        
    if parent != os.environ['SHOTS_DIR']:
        raise Exception("Shot folders must be created in "+os.environ['SHOTS_DIR'])
    
    new_dir = os.path.join(parent, name)
    print 'creating :'+new_dir
    addProjectFolder(parent, name)
    addVersionedFolder(new_dir, 'animation', -1)
    addVersionedFolder(new_dir, 'lighting', 5)
    addVersionedFolder(new_dir, 'compositing', 5)
    addProjectFolder(new_dir, 'animation_cache')
    addProjectFolder(os.path.join(new_dir, 'animation_cache'), 'abc')
    addProjectFolder(os.path.join(new_dir, 'animation_cache'), 'geo_sequences')
    addProjectFolder(os.path.join(new_dir, 'animation_cache'), 'point_cache')
    addProjectFolder(new_dir, 'playblasts')
    addProjectFolder(new_dir, 'renders')
    addProjectFolder(os.path.join(new_dir, 'renders'), 'lighting')
    addProjectFolder(os.path.join(new_dir, 'renders'), 'compositing')

def createNewPrevisFolders(name):
    parent = os.environ['PREVIS_DIR']
    # This is basically the same as "createNewShotFolders" method
    # doesn't include a lighting folder; may need to add/remove additional folders for production
    if parent != os.environ['PREVIS_DIR']:
        raise Exception("Shot folders must be created in "+os.environ['PREVIS_DIR'])
    
    new_dir = os.path.join(parent, name)
    print 'creating :'+new_dir
    addProjectFolder(parent, name)
    addVersionedFolder(new_dir, 'animation', -1)
    addVersionedFolder(new_dir, 'compositing', 5)
    addProjectFolder(new_dir, 'animation_cache')
    addProjectFolder(os.path.join(new_dir, 'animation_cache'), 'abc')
    addProjectFolder(os.path.join(new_dir, 'animation_cache'), 'geo_sequences')
    addProjectFolder(new_dir, 'playblasts')
    addProjectFolder(new_dir, 'renders')
    addProjectFolder(os.path.join(new_dir, 'renders'), 'lighting')
    addProjectFolder(os.path.join(new_dir, 'renders'), 'compositing')