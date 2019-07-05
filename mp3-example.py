#!/usr/bin/env python2

import sys

import ao
import mad

# The Mad audio library we're using expects to be given a file object, but
# we're not dealing with files, we're reading audio data over the network.  We
# use this object to trick it.  All it really wants from the file object is the
# read() method, so we create this wrapper with a read() method for it to
# call, and it won't know the difference.
# You probably don't need to modify this.
class mywrapper(object):
    def __init__(self):
        self.mf = None
        self.data = ""

    # When it asks to read a specific size, give it that many bytes, and
    # update our remaining data.
    def read(self, size):
        result = self.data[:size]
        self.data = self.data[size:]
        return result

def main():
    # Open the audio device.
    dev = ao.AudioDevice('pulse')

    # Create a wrapper object.
    wrap = mywrapper()

    # Open an MP3 file and read in all the data.
    # For you, this data will come in over the network from the server.
    f = open(sys.argv[1], 'r')
    data = f.read()
    f.close()

    # Hand off the data to the wrapper object and use it to create a new MAD
    # library decoder.  For your client, you will be appending chunks of data
    # to the end of wrap.data in your receiver thread while the player thread
    # is removing and playing data from the front of it.
    wrap.data = data
    print(data)
    wrap.mf = mad.MadFile(wrap)

    # Play the file.
    while True:
        buf = wrap.mf.read()
        if buf is None:  # eof
            break
        dev.play(buffer(buf), len(buf))

if __name__ == '__main__':
    main()
