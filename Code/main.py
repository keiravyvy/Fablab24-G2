from buzzer_music import music
from time import sleep
#    https://onlinesequencer.net/1696155 Undertale - Heartache
song = '0 C5 3 41;3 C5 1 41;4 D5 4 41;8 C5 4 41;12 F5 4 41;16 E5 8 41;24 C5 3 41;27 C5 1 41;28 D5 4 41;32 C5 4 41;36 G5 4 41;40 F5 8 41;48 C5 3 41;51 C5 1 41;52 C6 4 41;56 A5 4 41;60 F5 4 41;64 E5 4 41;68 D5 4 41;72 A#5 3 41;75 A#5 1 41;76 A5 4 41;80 F5 4 41;84 G5 4 41;88 F5 8 41'


"""
Find a piece of music on onlinesequencer.net, click edit,
then select all notes with CTRL+A and copy them with CTRL+C

Paste string as shown above after removing ";:" from
the end and "Online Sequencer:120233:" from the start
"""

from machine import Pin
import machine

#One buzzer on pin 0
mySong = music(song, pins=[Pin("GP15")])

#Four buzzers
#mySong = music(song, pins=[Pin(0),Pin(1),Pin(2),Pin(3)])
buffer = 0
elapsedTime=0
motor = machine.ADC(Pin(26))
val = motor.read_u16()
is_playing = False
while True:
    val = motor.read_u16()
    
    if(val > 1000 or val < 2):
        buffer = elapsedTime + 0.2
        
    if(elapsedTime < buffer):
        if(not is_playing):
            mySong.resume()
            is_playing= True
    else:
        mySong.stop()
        is_playing = False
    mySong.tick()
    elapsedTime += 0.04
    
    print("Motor: ",val, "Buffer: ", buffer, "elapsed: ", elapsedTime)
    sleep(0.04)