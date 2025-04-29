import csv
import random
from tkinter import *
from functools import partial  # to prevent unwanted windows
file = open("artists.csv", "r")
all_artists = list(csv.reader(file, delimiter=","))
file.close()

# remove first row
all_artists.pop(0)

print(all_artists)

round_artists = []
monthly_listeners = []

# loop until we have two artists CHANGE THE LOOP
while len(round_artists) < 2:
    # pick a random artist from the list
    random_artist = random.choice(all_artists)

    if random_artist not in round_artists:
        # add artist to the list for this round
        round_artists.append(random_artist)
        # add their monthly listeners to be compared
        monthly_listeners.append(random_artist[1])

highest_monthly_listeners = max(monthly_listeners)
answer = round_artists[monthly_listeners.index(highest_monthly_listeners)]
answer_name = answer[0]
print(highest_monthly_listeners)
print(answer)
print(answer_name)
print(round_artists)
print(monthly_listeners)
