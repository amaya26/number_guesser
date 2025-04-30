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
highest_monthly_listeners = max(round_monthly_listeners)
# find the lowest number of the artists for this round
lowest_monthly_listeners = min(round_monthly_listeners)

# correct answer is round_artists[the list position of the highest monthly listeners]
# (match the highest monthly listeners to the corresponding artist)
correct_answer = round_artists[round_monthly_listeners.index(highest_monthly_listeners)]
# find the incorrect answer
incorrect_answer = round_artists[round_monthly_listeners.index(lowest_monthly_listeners)]

# correct_answer contains name and number. Get name on its own
correct_artist_name = correct_answer[0]
# get name on its own
incorrect_artist_name = incorrect_answer[0]

print(round_monthly_listeners.index(highest_monthly_listeners))
print(round_monthly_listeners.index(lowest_monthly_listeners))
print(highest_monthly_listeners)
print(correct_answer)
print(correct_artist_name)
print(incorrect_answer)
print(incorrect_artist_name)
print(round_artists)
print(round_monthly_listeners)
