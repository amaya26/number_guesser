import csv
import random
from tkinter import *
from functools import partial  # to prevent unwanted windows


# helper functions go here
def get_artists():
    """
    Retrieves artists from csv file
    :return: list of artists where each list item has the
    artist name and monthly listeners
    """

    file = open("artists_testing.csv.csv", "r")
    all_artists_list = list(csv.reader(file, delimiter=","))
    file.close()

    # remove first row
    all_artists_list.pop(0)

    return all_artists_list


all_artists = get_artists()

round_artists = []
round_monthly_listeners = []

# loop until we have two artists
while len(round_artists) < 2:
    # pick a random artist from the list
    random_artist = random.choice(all_artists)

    if random_artist not in round_artists:
        # add artist to the list for this round
        round_artists.append(random_artist)
        # add their monthly listeners to be compared
        round_monthly_listeners.append(int(random_artist[1]))

# find the highest number of monthly listeners of the two artists for this round
highest_monthly_listeners = max(round_monthly_listeners)
# find the lowest number of the artists for this round
lowest_monthly_listeners = min(round_monthly_listeners)

# correct answer is round_artists[the list position of the highest monthly listeners]
# (match the highest monthly listeners to the corresponding artist)
correct_answer = round_artists[round_monthly_listeners.index(highest_monthly_listeners)]
# find the incorrect answer
incorrect_answer = round_artists[round_monthly_listeners.index(lowest_monthly_listeners)]

print(f"Artists for this round: {round_artists}")
print(f"Correct answer: {correct_answer}")
print(f"Incorrect answer: {incorrect_answer}")