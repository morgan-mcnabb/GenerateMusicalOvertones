# Simulation Steps
# 1. Store the first value from the ring buffer in the samples buffer
# 2. Calculate the average of the first two elements in the ring buffer
# 3. Multiply this average value by an attenuation factor
# 4. Append this value to the end of the ring buffer
# 5. Remove the first element of the ring buffer
import wave
import math
import numpy as np


def main():
    sRate = 44100
    nSamples = sRate * 5

    # create an array of amplitude values
    x = np.arange(nSamples)/float(sRate)
    vals = np.sin(2.0 * math.pi * 220.0 * x)

    # Scale the sine wave values to 16-bit values
    data = np.array(vals*32767, 'int16').tobytes()

    file = wave.open('sine220.wav', 'wb')

    # PARAMS
    # 1 = Mono
    # 2 = 2-byte (16-bit)
    # sRate = Sampling rate
    # nSamples = length in seconds of .wav file
    # uncompressed = uncompressed format
    file.setparams((1, 2, sRate, nSamples, 'NONE', 'uncompressed'))

    file.writeframes(data)
    file.close()


if __name__ == '__main__':
    main()
