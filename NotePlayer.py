import pygame
import random


class NotePlayer:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()

        # dictionary of notes
        self.notes = {}

    # add a note
    def add(self, fileName):
        self.notes[fileName] = pygame.mixer.Sound(fileName)

    # play a note
    def play(self, fileName):
        try:
            self.notes[fileName].play()
        except Exception as exc:
            print(fileName + " not found!")

    # play a random note
    def playRandom(self):
        index = random.randint(0, len(self.notes)-1)
        note = list(self.notes.values())[index]
        note.play()
