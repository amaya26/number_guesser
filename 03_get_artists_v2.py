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
        print(f"Artist to add: {random_artist}")
        print("Not already in list")
        print()
    else:
        print(f"Artist to add: {random_artist}")
        print("Already in list")
        print()

print(f"All artists: {all_artists}")
print(f"All artists for this round: {round_artists}")

