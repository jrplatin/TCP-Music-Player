#!/usr/bin/env python

import os
import socket
import struct
import sys
import urllib
import pickle

from threading import Lock, Thread


QUEUE_LENGTH = 10
SEND_BUFFER = 4096

songNameToData = {}

# per-client struct
class Client:
    songRequest = ""
    currentCommand = ""
    def __init__(self):
        self.lock = Lock()
    def setSong(songName):
        songRequest = songName
    def getCurrentSong():
        return songRequest
    def setCommand(command):
        currentCommand = command
    def getCommand():
        return currentCommand


# TODO: Thread that sends music and lists to the client.  All send() calls
# should be contained in this function.  Control signals from client_read could
# be passed to this thread through the associated Client object.  Make sure you
# use locks or similar synchronization tools to ensure that the two threads play
# nice with one another!
def client_write(client):
    command = client.getCommand()
    song = client.getCurrentSong()
    

    if(command == "list"):
        data=pickle.dumps(songlist)
        socket.send(data)
    elif(command == "play"):
        relData = songNameToData[song]
        socket.send(relData)

    data = songNameToData[song]
    socket.send(data)

# TODO: Thread that receives commands from the client.  All recv() calls should
# be contained in this function.
def client_read(client):
    command, song = socket.receive()
    if(command == "list"):
        client.setCommand("list")
        client_write(client)
    elif(command == "play"):
        client.setCommand("play")
        client.setSong(song)
        client_write(client)
    elif(command == "stop")
        client.setCommand("stop")
        client_write(client)
    else:
        print("Bye!")
        exit(0)


def get_mp3s(musicdir):
    print("Reading music files...")
    songs = []
    for filename in os.listdir(musicdir):
        if not filename.endswith(".mp3"):
            continue
        else:
            

        # TODO: Store song metadata for future use.  You may also want to build
        # the song list once and send to any clients that need it.    
        curDir = os.getcwd() + "\\" + filename
        songFile =  open(curDir, 'r')
        filedata = songFile.read()

        songName = filename.split(".mp3")[0]
        songNameToData[songName] = filedata
        songs.append(songName)

    print("Found {0} song(s)!".format(len(songs)))

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python server.py [port] [musicdir]")
    if not os.path.isdir(sys.argv[2]):
        sys.exit("Directory '{0}' does not exist".format(sys.argv[2]))

    port = int(sys.argv[1])
    songs, songlist = get_mp3s(sys.argv[2])
    threads = []

    # TODO: create a socket and accept incoming connections
    while True:
        client = Client()
        t = Thread(target=client_read, args=(client))
        threads.append(t)
        t.start()
        t = Thread(target=client_write, args=(client))
        threads.append(t)
        t.start()
    s.close()


if __name__ == "__main__":
    main()