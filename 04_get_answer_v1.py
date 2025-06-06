import csv
import random


file = open("artists_testing.csv", "r")
all_artists = list(csv.reader(file, delimiter=","))
file.close()

# remove first row
all_artists.pop(0)

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

print(f"Artists for this round: {round_artists}")
print(f"Correct answer: {correct_answer}")
print(f"Incorrect answer: {incorrect_answer}")
