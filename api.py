#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import *
from mcstatus import MinecraftServer
from valve.source.a2s import ServerQuerier

mc_server = MinecraftServer.lookup("pegelcraft.de")
gmod_server = ServerQuerier(["gmod.pegelf.de", 27015])

app = Flask(__name__)

@app.route("/mc", methods=["GET"])
def get_mc_server():
    query = mc_server.query()
    blub = {}
    blub["motd"] = query.motd
    blub["map"] = query.map
    blub["players"] = query.players.names
    blub["max_players"] = query.players.max
#    blub["plugins"] = query.software.plugins
    blub["version"] = query.software.version
    blub["brand"] = query.software.brand
    return Response(json.dumps(blub,indent=4, separators=(',', ': ')), mimetype='application/json')

@app.route("/gmod", methods=["GET"])
def get_gmod_server():
    blub = {}
    for x in gmod_server.get_info():
        if x in ["bot_count", "protocol", "response_type", "folder"]:
            continue
        elif x in ["server_type", "platform"]:
            blub[x] = str(gmod_server.get_info()[x])
        elif x == "password_protected":
            blub[x] = (gmod_server.get_info()[x] == 1)
        else:
            blub[x] = gmod_server.get_info()[x]
    blub["players"] = gmod_server.get_players()["players"]
    return Response(json.dumps(blub, indent=4, separators=(',', ': ')), mimetype='application/json')
