import utilities

#################################################################################
# Checkout
#################################################################################
def _createCheckoutInfoFile(dirPath, coPath, version, timestamp, lock):
	"""
	Creates a .checkoutInfo file in the directory specified by dirPath
	@precondition: dirPath is a valid path
	@postcondition: dirPath/.checkoutInfo contains complete [Checkout] section
	"""
	chkoutInfo = ConfigParser()
	chkoutInfo.add_section("Checkout")
	chkoutInfo.set("Checkout", "checkedoutfrom", coPath)
	chkoutInfo.set("Checkout", "checkouttime", timestamp)
	chkoutInfo.set("Checkout", "version", version)
	chkoutInfo.set("Checkout", "lockedbyme", str(lock))
	
	_writeConfigFile(os.path.join(dirPath, ".checkoutInfo"), chkoutInfo)

def isCheckedOut(dirPath):
	nodeInfo = os.path.join(dirPath, ".nodeInfo")
	if not os.path.exists(nodeInfo):
		return False
	cp = ConfigParser()
	cp.read(nodeInfo)
	return cp.getboolean("Versioning", "locked")

def checkedOutByMe(dirPath):
	nodeInfo = os.path.join(dirPath, ".nodeInfo")
	if not os.path.exists(nodeInfo):
		return False
	cp = ConfigParser()
	cp.read(nodeInfo)
	return cp.get("Versioning", "lastcheckoutuser") == getUsername()

def getFilesCheckoutTime(filePath):
	checkoutInfo = os.path.join(filePath, ".checkoutInfo")
	#print checkoutInfo
	if not os.path.exists(checkoutInfo):
		raise Exception("No checkout info available")
	cp = ConfigParser()
	cp.read(checkoutInfo)
	return cp.get("Checkout", "checkouttime")

def canCheckout(coPath):
	result = True
	if not os.path.exists(os.path.join(coPath, ".nodeInfo")):
		result = False
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(coPath, ".nodeInfo"))
	if nodeInfo.get("Versioning", "locked") == "True":
		result = False
	return result

def getCheckoutDest(coPath):
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(coPath, ".nodeInfo"))
	version = nodeInfo.get("Versioning", "latestversion")
	return os.path.join(getUserCheckoutDir(), os.path.basename(os.path.dirname(coPath))+"_"+os.path.basename(coPath)+"_"+("%03d" % int(version)))

def lockedBy(logname):
    """
    Returns a tuple containing the logname and the real name

    Raises a generic exception if real name cannot be determined.
    """

    try: # Throws KeyError exception when the name cannot be found
        p = pwd.getpwnam( str(logname) )
    except KeyError as ke: # Re-throws KeyError as generic exception
        raise Exception( str(ke) )

    return p.pw_name, p.pw_gecos # Return lockedBy tuple

def checkout(coPath, lock):
	"""
	Copies the 'latest version' from the src folder into the local directory
	@precondition: coPath is a path to a versioned folder
	@precondition: lock is a boolean value
	
	@postcondition: A copy of the 'latest version' will be placed in the local directory
		with the name of the versioned folder
	@postdondition: If lock == True coPath will be locked until it is released by checkin
	"""
	#if not os.path.exists(os.path.join(coPath, ".nodeInfo")):
	if not isVersionedFolder(coPath):
		raise Exception("Not a versioned folder.")
	
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(coPath, ".nodeInfo"))
	if nodeInfo.get("Versioning", "locked") == "False":
		version = nodeInfo.getint("Versioning", "latestversion")
		toCopy = os.path.join(coPath, "src", "v"+("%03d" % version))
		dest = getCheckoutDest(coPath)
		
		if(os.path.exists(toCopy)):
			try:
				shutil.copytree(toCopy, dest) # Make the copy
			except Exception:
				print "asset_mgr_utils, checkout: Could not copy files."
				raise Exception("Could not copy files.")
			timestamp = time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime())
			nodeInfo.set("Versioning", "lastcheckoutuser", getUsername())
			nodeInfo.set("Versioning", "lastcheckouttime", timestamp)
			nodeInfo.set("Versioning", "locked", str(lock))
			
			_writeConfigFile(os.path.join(coPath, ".nodeInfo"), nodeInfo)
			_createCheckoutInfoFile(dest, coPath, version, timestamp, lock)
		else:
			raise Exception("Version doesn't exist "+toCopy)
	else:
		whoLocked = nodeInfo.get("Versioning", "lastcheckoutuser")
		whenLocked = nodeInfo.get("Versioning", "lastcheckouttime")
		logname, realname = lockedBy(whoLocked)
		whoLocked = 'User Name: ' + logname + '\nReal Name: ' + realname + '\n'
		raise Exception("Can not checkout. Folder is locked by:\n\n"+ whoLocked+"\nat "+ whenLocked)
	return dest

def unlock(ulPath):
	
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(ulPath, ".nodeInfo"))
	nodeInfo.set("Versioning", "locked", "False")

	toCopy = getCheckoutDest(ulPath)
	dirname = os.path.basename(toCopy) 
	parentPath = os.path.join(os.path.dirname(toCopy), ".unlocked")
	if not (os.path.exists(parentPath)):
		os.mkdir(parentPath)

	os.system('mv -f '+toCopy+' '+parentPath+'/')
	_writeConfigFile(os.path.join(ulPath, ".nodeInfo"), nodeInfo)
	return 0;

def isLocked(ulPath):
	nodeInfo = ConfigParser()
	nodeInfo.read(os.path.join(ulPath, ".nodeInfo"))
	if nodeInfo.get("Versioning", "locked") == "False":
		return False;
	
	return True;