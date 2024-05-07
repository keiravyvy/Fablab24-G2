from buzzer_music import music
from time import sleep

#    https://onlinesequencer.net/1696155 Undertale - Heartache
song = "0 C5 3 41;3 C5 1 41;4 D5 4 41;8 C5 4 41;12 F5 4 41;16 E5 8 41;24 C5 3 41;27 C5 1 41;28 D5 4 41;32 C5 4 41;36 G5 4 41;40 F5 8 41;48 C5 3 41;51 C5 1 41;52 C6 4 41;56 A5 4 41;60 F5 4 41;64 E5 4 41;68 D5 4 41;72 A#5 3 41;75 A#5 1 41;76 A5 4 41;80 F5 4 41;84 G5 4 41;88 F5 8 41"


"""
Find a piece of music on onlinesequencer.net, click edit,
then select all notes with CTRL+A and copy them with CTRL+C

Paste string as shown above after removing ";:" from
the end and "Online Sequencer:120233:" from the start
"""

from machine import Pin
import machine

# One buzzer on pin 0
mySong = music(song, pins=[Pin("GP1")])
print("Started")
# Four buzzers
# mySong = music(song, pins=[Pin(0),Pin(1),Pin(2),Pin(3)])
buffer = 0
elapsedTime = 0

low_threshold = 15000
high_threshold = 40000
min_threshold = 300
motor = machine.ADC(Pin(26))
low_led = machine.Pin("GP20", machine.Pin.OUT)
med_led = machine.Pin("GP19", machine.Pin.OUT)
high_led = machine.Pin("GP18", machine.Pin.OUT)


low_led.off()
high_led.off()

is_playing = False
val = 0

while True:
    val = ((val * 4) + motor.read_u16()) / 5
    print("Motor: ", val, "Buffer: ", buffer, "elapsed: ", elapsedTime)
    if val < min_threshold:
        low_led.off()
        high_led.off()

    if val > high_threshold:
        high_led.on()
        low_led.off()

    if min_threshold < val < low_threshold:
        low_led.on()
        high_led.off()

    if low_threshold < val < high_threshold:
        buffer = elapsedTime + 0.2
        low_led.off()
        high_led.off()

    if elapsedTime < buffer:
        if not is_playing:
            mySong.resume()
            is_playing = True
            med_led.on()
            low_led.off()
            high_led.off()
    else:
        mySong.stop()
        is_playing = False
        med_led.off()
    mySong.tick()
    elapsedTime += 0.04

    sleep(0.04)