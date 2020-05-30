import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import urllib.parse
import secrets
import json
import os
import re

cred = credentials.Certificate("sheep16-spacesheep-firebase-adminsdk-qjr6i-1839d2596a.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

arr = os.listdir("missions/")
type = []

for a in arr:
	type = a.split('.')
	if(type[1] == "md"):
		file = open("missions/" + a, "+r")
		content = file.read()
		match = re.search("---(.|\n)*?---", content)
		target = match.group()
		
		target = re.sub('"', '\\"', target)
		target = re.sub("---", "{", target, 1)
		target = re.sub("---", "}", target, 1)
		target = re.sub("\n  - ", ", ", target)
		target = re.sub(":, ", "\":[", target)
		target = re.sub("\n    ", ", ", target)
		target = re.sub(r"(\[.*)", r"\1]", target)
		target = re.sub("\n", "\",\n\"", target)
		target = re.sub(", ", "\", \"", target)
		target = re.sub(": ", "\":\"", target)
		target = re.sub("\[", "[\"", target)
		target = re.sub("\]\"", "\"]", target)
		target = re.sub("\{\",", "{", target)
		target = re.sub(",\n\"\}", "\n}", target)
		target = re.sub("\"label", "{\"label", target)
		target = re.sub(r"(\"href\":\".*\")", r"\1}", target)
		target = re.sub(", \{", "}, {", target)
		target = re.sub(",\n", ",\n\"type\":\"mission\",\n", target, 1) 
		target = re.sub(",\n", ",\n\"type\":\"mission\",\n", target, 1) 
		target = re.sub(",\n", ",\n\"from\":\"https://raw.githubusercontent.com/sheepsixteen/missions/master/" + urllib.parse.quote(type[0]) + "\",\n", target, 1)		

		match = re.search(r"\"difficulty\":\"([0-9]+)\"", target)
		difficulty = match.group()
		difficulty = int(difficulty.split('"')[3])

		d = json.loads(target)
		d["difficulty"] = difficulty
		
		print(d)
		
		id = secrets.token_urlsafe(20)

		doc_ref = db.collection('example').document(id)
		doc_ref.set(d)
