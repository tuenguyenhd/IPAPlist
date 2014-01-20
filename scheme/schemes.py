import tempfile
import zipfile
import os.path
from subprocess import Popen, PIPE
import xml.etree.ElementTree as ET
import plistlib
import sys

def plist_to_json(filename):
	return plistlib.readPlist(filename)	
		
def scheme_from_json(json):
	try:
		scheme_arrays = json["CFBundleURLTypes"][0]
		scheme_arrays = scheme_arrays["CFBundleURLSchemes"]
		return scheme_arrays
	except Exception as e:
		return None
						
def unzip_schemes(path):
	zfile = zipfile.ZipFile(path)
	scheme_arrays = None
	for name in zfile.namelist():		
		if ".app/Info.plist" in name:					
			tup = tempfile.mkstemp(suffix = '.plist')
			fd = os.fdopen(tup[0], "w")				
			fd.write(zfile.read(name))
			fd.close()
			scheme_arrays = scheme_from_json(plist_to_json(tup[1]))
			os.remove(tup[1])
	zfile.close()
	return scheme_arrays


if(len(sys.argv) > 1):
	print unzip_schemes(sys.argv[1])
