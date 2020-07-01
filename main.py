# Simulation Steps
# 1. Store the first value from the ring buffer in the samples buffer
# 2. Calculate the average of the first two elements in the ring buffer
# 3. Multiply this average value by an attenuation factor
# 4. Append this value to the end of the ring buffer
# 5. Remove the first element of the ring buffer
import wave
import math
import numpy as np
import random
from collections import deque


# generate a note of a given frequency with Karplus-Strong algorithm
def generateNote(freq):
    nSamples = 44100
    sampleRate = 44100
    length = int(sampleRate / freq)

    # initialize the ring buffer with random values between -0.5 and 0.5
    ringBuffer = deque([random.random() - 0.5 for i in range(length)])

    # initialize the samples buffer
    samplesBuffer = np.array([0]*nSamples, 'float32')

    for i in range(nSamples):
        # first element in the ring buffer is copied to the samples buffer
        samplesBuffer[i] = ringBuffer[0]

        # Apply the attenuation and calculate the average
        average = 0.996*0.5*(ringBuffer[0] + ringBuffer[1])
        ringBuffer.append(average)
        ringBuffer.popleft()

    # convert the samples to 16-bit values
    samples = np.array(samplesBuffer*32767, 'int16')
    return samples.tobytes()


def main():
    holder = generateNote(100)


if __name__ == '__main__':
    main()
