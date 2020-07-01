# Simulation Steps
# 1. Store the first value from the ring buffer in the samples buffer
# 2. Calculate the average of the first two elements in the ring buffer
# 3. Multiply this average value by an attenuation factor
# 4. Append this value to the end of the ring buffer
# 5. Remove the first element of the ring buffer
import sys, os
import time,random
import wave, argparse
from NotePlayer import NotePlayer
import numpy as np
import pygame
from collections import deque
from matplotlib import pyplot as plt


# bool for showing the plot of the algorithm in action
gShowPlot = False


def WriteWAV(fileName, soundData):

    # open the file
    file = wave.open(fileName, 'wb')

    # channel 1 = MONO
    nChannels = 1

    # 2 = 2 bytes (16-bit)
    sampleWidth = 2

    frameRate = 44100
    nFrames = 44100

    file.setparams((nChannels, sampleWidth, frameRate, nFrames, 'NONE', 'noncompressed'))

    file.writeframes(soundData)
    file.close()


# generate a note of a given frequency with Karplus-Strong algorithm
def GenerateNote(freq):
    nSamples = 44100
    sampleRate = 44100
    length = int(sampleRate / freq)

    # initialize the ring buffer with random values between -0.5 and 0.5
    ringBuffer = deque([random.random() - 0.5 for i in range(length)])

    if gShowPlot:
        axline, = plt.plot(ringBuffer)

    # initialize the samples buffer
    samplesBuffer = np.array([0]*nSamples, 'float32')

    for i in range(nSamples):
        # first element in the ring buffer is copied to the samples buffer
        samplesBuffer[i] = ringBuffer[0]

        # Apply the attenuation and calculate the average
        average = 0.995*0.5*(ringBuffer[0] + ringBuffer[1])
        ringBuffer.append(average)
        ringBuffer.popleft()
        if gShowPlot:
            if i % 1000 == 0:
                axline.set_ydata(ringBuffer)
                plt.draw()

    # convert the samples to 16-bit values
    samples = np.array(samplesBuffer*32767, 'int16')
    return samples.tobytes()


def main():

    global gShowPlot

    # notes of a pentatonic minor scale
    # piano C4-E(b)-F-G-B(b)
    pmNotes = {'C4': 262, 'Eb': 311, 'F': 349, 'G': 391, 'Bb': 466}

    parser = argparse.ArgumentParser(description="Generating sounds with Karplus Strong Algorithm")

    # add arguments
    parser.add_argument('--display', action='store_true', required=False)
    parser.add_argument('--play', action='store_true', required=False)
    parser.add_argument('--piano', action='store_true', required=False)

    args = parser.parse_args()

    # show the algorithm working if flag is set
    if args.display:
        gShowPlot = True
        plt.ion()

    # create the note player
    notePlayer = NotePlayer()

    print('creating notes...')
    for name, freq in list(pmNotes.items()):
        fileName = name + '.wav'
        if not os.path.exists(fileName) or args.display:
            soundData = GenerateNote(freq)
            print('creating ' + fileName + '...')
            WriteWAV(fileName, soundData)
        else:
            print("fileName already created. Skipping... ")

        # add note to player
        notePlayer.add(name + '.wav')

        # play note if display flag is set
        if args.display:
            notePlayer.play(name + '.wav')
            time.sleep(0.5)

    # play a random note
    if args.play:
        while True:
            try:
                notePlayer.playRandom()
                # rest - 1 to 8 beats
                rest = np.random.choice([1, 2, 4, 8], 1, p=[0.15, 0.7, 0.1, 0.05])

                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()

    if args.piano:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    print("key pressed")
                    notePlayer.playRandom()
                    time.sleep(0.5)


if __name__ == '__main__':
    main()
