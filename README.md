# Project 6: Streaming Music Service

In this project, you'll be designing and implementing a protocol of your own design to build a streaming music service.
In class, we discussed a few approaches to building such a service: simple HTTP gets, a custom streaming protocol like RTSP, or DASH-like chunking via HTTP.
For this project, we want you to try your hand at a custom protocol to learn all of the concerns that go into constructing one.
Note that while RTSP is a good strawman, it is likely *much* more complicated than you need for this project.

Since you will be developing the protocol, client, and server, there is no single correct design or architecture.
This is different from previous projects, where you have seen and implemented several types of protocols -- now you get to decide how to apply the patterns you've seen in a new scenario!


### Requirements

* Your protocol should be implemented directly on top of sockets.  You should not, for instance, use an HTTP protocol or implementation.

* We have provided skeleton code for a threaded client and server in Python.  Feel free to start from scratch in a different language or with a different architecture (e.g.,  select() statements).  If you choose a different language, you will be responsible for finding libraries that can play mp3 files.

* Your server should be able to handle multiple clients simultaneously.  They should be able join and leave at any time, and the server should continue to operate seamlessly.

* The client should be able to stream, i.e., start playing music before the mp3 has been downloaded.  Note that mp3s are designed exactly for this purpose!  If you start feeding  mp3 data frames to a music player, it will be able to play without needing the entire file.

* Your client should be interactive and it should know how to handle at least the following commands:
    * `list`: Retrieve a list of songs that are available on the server, along with their ID numbers.
    * `play [song number]`: Begin playing the song with the specified ID number. If another song is already playing, the client should switch immediately to the new one.
    * `stop`: Stops playing the current song, if there is one playing.

* The client should not cache data. In other words, if the user tells the client to get a song list or play a song, the two should exchange messages to facilitate this. Don't retrieve an item from the server once and then repeat it back again on subsequent requests.

* One of the parameters to your server should be a path to a directory that contains audio files. Within this directory, you may assume that any file ending in ".mp3" is an mp3 audio file. I have provided two files as a start.  Feel free to use those or your own mp3 files for testing. **Please do not submit audio files to Canvas!**

* You are allowed to develop and demo this project outside of the Vagrant VM, but we have already set up the Vagrant VM to be compatible with playing audio programmatically.  It may also facilitate interoperability between partners with different OSes and installed packages.


### Getting started

Download the project6.zip file and extract it in the same way as previous projects.  The directory contains this README, a folder of music, scaffolding for a client and server, and a test file for playing music in Python.

1. The first step is to ensure that you can play music programmatically.  For that, we want to upgrade your Vagrant VM to the most recent drivers:

    ```shell
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y linux-modules-extra-`uname -r`
    ```

2. Now restart the VM with `vagrant halt; vagrant up; vagrant ssh` in your host OS.

3. Initialize and turn up the sound with:
    ```shell
    sudo alsactl init
    alsamixer # use arrow keys to turn up master volume
    ```

4. Test using the provided script.
    ```shell
    cd /vagrant/project6
    python mp3-example.py music/Beethoven.mp3
    # make sure your host OS has its volume turned up as well
    ```

### Helpful hints

* My reference solution requires ~300 lines of code.  Note that less code is typically correlated with better results as it indicates a simpler and more well-thought-out protocol.

* When using threads, be very careful with thread safety.  Python has a threading module that gives you threads, locks, and condition variables.  Note that socket `send`s/`recv`s are thread safe, meaning you can have a thread send() and another thread recv() concurrently without the help of locks, etc.  You probably don't want to execute *split* sends (or recvs) for the same connection in two different threads as messages can become interleaved.

* The python struct module is very useful for serializing and deserializing arbitrary datatypes.

* It's possible that a client closes a connection just before your server attempts to send to it. In this case, by default, two things will happen: 1) your process will receive the SIGPIPE signal, which by default, kills your process, and 2) send will return an error and set errno to EPIPE to indicate the connection (pipe) was broken. Obviously you don't want (1) to occur, since you still want to service other clients. Luckily, we can easily prevent that signal by using the that extra "flags" parameter to send that we've been ignoring thus far. By setting the flags to MSG_NOSIGNAL, the kernel will only do (2), which is a much more convenient way for you to detect and handle a client disconnection.

* Test your code in small increments. It's much easier to localize a bug when you've only changed a few lines.

* If you want your client to begin playing a new file, you need to create a new MadFile object. This tells mad (our audio library) to interpret the next bytes as the beginning of a new file (which includes some metadata) rather than the middle of the previously playing file.


### Submission and grading

#### Part A (Completion grade)

Please plan out the protocol design and fill out the ProtocolDescription.txt file.  You don't need to write a lot, but your protocol should be well thought out and well described.

#### Part B

Submit the project by uploading your modified client and server files to Canvas by the deadline.  Please do not submit audio files to Canvas!  Your grade will be based on a final demo that you can sign up for here: [https://calendly.com/liuv/p6demo](https://calendly.com/liuv/p6demo).  Demos will use the uploaded code.  Note that you cannot use slip hours past your scheduled demo slot.

If none of the listed times work (for instance if you already booked tickets home), let me know and we can arrange a different time.


### Acknowledgements

Adapted with permission from Kevin Webb at Swarthmore College
