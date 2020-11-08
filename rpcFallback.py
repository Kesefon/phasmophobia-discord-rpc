#! /bin/env python3
#change steam launch options to:
#/path/to/this.script %command%

import discord_rpc
import string
import inotify.adapters 
import os
import time
from subprocess import Popen
import sys

client_id = '774597065569075250'
mapNames = ["Starting", "Menu", "41 Tanglewood Street", "Asylum", "67 Edgefield Street", "56 Ridgeview Road", "James Brownstone High School", "Bleasdale Farmhouse", "Grafton Farmhouse"]
    #start = 0
    #menu = 1
    #tanglewood = 2
    #asylum = 3
    #edgefield = 4
    #ridgeview = 5
    #highschool = 6
    #bleasdale = 7
    #grafton = 8

#start Game
del sys.argv[0]
game = Popen(sys.argv)
phasmophobiaDir = os.path.dirname(sys.argv[2])

#prepare Discord-RPC
def readyCallback(current_user):
    print('Our user: {}'.format(current_user))

def disconnectedCallback(codeno, codemsg):
    print('Disconnected from Discord rich presence RPC. Code {}: {}'.format(
        codeno, codemsg
    ))
    exit()

def errorCallback(errno, errmsg):
    print('An error occurred! Error {}: {}'.format(
        errno, errmsg
    ))
    exit()

callbacks = {
    'ready': readyCallback,
    'disconnected': disconnectedCallback,
    'error': errorCallback,
}

#start Discord-RPC
discord_rpc.initialize(client_id, callbacks=callbacks, auto_update_connection=True)
discord_rpc.register_game(client_id, steam_id="739630")

#start watching level files
iNotifier = inotify.adapters.Inotify()
for i in range(9):
    print(os.path.join(phasmophobiaDir, 'Phasmophobia_Data', ('level' + str(i))))
    iNotifier.add_watch(os.path.join(phasmophobiaDir, 'Phasmophobia_Data', ('level' + str(i))), mask=0x00000020 )

for event in iNotifier.event_gen():
    if event != None:
        (_, type_names, path, filename) = event
        levelNumber = int(path[-1])
        map = mapNames[levelNumber]

        discord_rpc.update_presence(**{
        'state': map,
        'large_image_key': map.lower().replace(' ', '_'),
        'start_timestamp': int(time.time()),
        })
        discord_rpc.run_callbacks()
        time.sleep(20)
    if game.poll() != None:
        discord_rpc.shutdown()
        exit()