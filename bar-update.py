#!/usr/bin/env python

import sys, csv, subprocess, os, json, requests
from time import gmtime, strftime

def process(command, new = False):
	if new:
		with open(os.devnull, "w") as fnull: result = subprocess.Popen(command, stdout = fnull, stderr = fnull)
	else:
		with open(os.devnull, "w") as fnull: result = subprocess.call(command, stdout = fnull, stderr = fnull)
def buildJSON(title, artist, album, artURL, station_name, loved, explainURL, songDuration = 0, songPlayed = 0):
	data = '{"title": ' + json.dumps(title) + ',"artist": ' + json.dumps(artist) + ',"album": ' + json.dumps(album) + ',"artURL": ' + json.dumps(artURL) + ',"station_name": ' + json.dumps(station_name) + ',"loved": ' + str(bool(loved)).lower() + ',"explainURL": ' + json.dumps(explainURL) + ', "songDuration": ' + str(songDuration) + ', "songPlayed": ' + str(songPlayed) + '}'
	return json.loads(data)
def sendRequest(url, method, songData):
	requests.post(url, params=dict(json=json.dumps(dict(method=method, id=1, songData=songData))))
www = os.path.dirname(os.path.abspath(__file__)) + "/"
url = "http://localhost:8080/api"

event = sys.argv[1]
lines = sys.stdin.readlines()
fields = dict([line.strip().split("=", 1) for line in lines])

artist = fields["artist"]
title = fields["title"]
album = fields["album"]
coverArt = fields["coverArt"]
rating = int(fields["rating"])
detailUrl = fields["detailUrl"].split('?dc')[0]
songDuration = fields["songDuration"]
songPlayed = fields["songPlayed"]
curStation = fields["stationName"]

if event == "songstart" or event == "songexplain":
	sendRequest(url, "SetSongInfo", buildJSON(title, artist, album,  coverArt, curStation,rating, detailUrl))
elif event == "songlove":
	sendRequest(url, "SetSongInfo", buildJSON(title, artist, album, coverArt, curStation,rating, detailUrl))
elif event == "usergetstations" or event == "stationcreate" or event == "stationdelete" or event == "stationrename":				# Code thanks to @officerNordBerg on GitHub
	stationCount = int(fields["stationCount"])
	stations = ""
	for i in range(0, stationCount):
		stations += "%s="%i + fields["station%s"%i] + "|"
	stations = stations[0:len(stations) - 1]
	open(www + "stationList", "w").write(stations)