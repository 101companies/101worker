#! /usr/bin/env python

from os import listdir
from os.path import isfile, join
from jsonschema import validate, exceptions 
import json

json_dump = {
	"missing_description": [],
	"invalid_description": []
	}

schema = json.load(open("../../schemas/moduleDescription.json","r"))

for moduleFolder in listdir("../"):
	if not isfile(moduleFolder):
		moduleDescPath = join("..",moduleFolder, "module.json")
		if isfile(moduleDescPath):
			try:
				validate(json.load(open(moduleDescPath,"r")), schema)
			except exceptions.ValidationError as error:
				json_dump["invalid_description"].append({"name":moduleFolder, "error_message": error.message})
		else:
			json_dump["missing_description"].append(moduleFolder)

dump_file = open("../../../101web/data/dumps/validateModuleDescriptions.json", "w")
dump_file.write(json.dumps(json_dump, sort_keys=True, indent=4, separators=(',', ': ')))
dump_file.close()