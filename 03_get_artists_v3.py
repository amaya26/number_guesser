import csv
import random
from tkinter import *
from functools import partial  # to prevent unwanted windows
file = open("artists.csv", "r")
all_artists = list(csv.reader(file, delimiter=","))
file.close()

# remove first row
all_artists.pop(0)

round_artists = []
round_monthly_listeners = []

# loop until we have two artists CHANGE THE LOOP
while len(round_artists) < 2:
    # pick a random artist from the list
    random_artist = random.choice(all_artists)

    if random_artist not in round_artists:
        # add artist to the list for this round
        round_artists.append(random_artist)
        # add their monthly listeners to be compared
        round_monthly_listeners.append(random_artist[1])

# find the highest number of monthly listeners of the two artists for this round
monthly_listeners1 = round_monthly_listeners[1]
monthly_listeners0 = round_monthly_listeners[0]

print(monthly_listeners0)
print(monthly_listeners1)
print(round_artists)

if monthly_listeners0 > monthly_listeners1:
    correct = round_artists.index(monthly_listeners0)
