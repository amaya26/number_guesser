import csv
import random
from tkinter import *
from functools import partial  # to prevent unwanted windows
file = open("artists_testing.csv", "r")
all_artists = list(csv.reader(file, delimiter=","))
file.close()

# remove first row
all_artists.pop(0)

round_artists = []
monthly_listeners = []

# loop until we have two artists CHANGE THE LOOP
while len(round_artists) < 2:
    # pick a random artist from the list
    random_artist = random.choice(all_artists)
    # add artist to the list for this round
    round_artists.append(random_artist)

print(f"All artists: {all_artists}")
print(f"All artists for this round: {round_artists}")
