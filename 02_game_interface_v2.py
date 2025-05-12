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

    file = open("artists.csv", "r")
    all_artists = list(csv.reader(file, delimiter=","))
    file.close()

    # remove first row
    all_artists.pop(0)

    return all_artists


def get_round_artists():
    """
    Choose two artists from larger list.
    :return: list of artists and correct answer (the highest monthly listeners)
    """

    all_artist_list = get_artists()

    round_artists = []
    round_monthly_listeners = []

    # loop until we have two artists CHANGE THE LOOP
    while len(round_artists) < 2:
        # pick a random artist from the list
        random_artist = random.choice(all_artist_list)

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

    # return both names
    return correct_artist_name, incorrect_artist_name


class StartGame:
    """
    Initial game interface (asks users how many rounds they would like to play)
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # create play button
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """
        Play(5)
        # Hide root window (ie hide rounds choice window)
        root.withdraw()


class Play:
    """
    Interface for playing the Colour Quest game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # body font for most labels...
        body_font = ("Arial", "12")

        # List for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), None, 0],
            ["Which artist has the most monthly listeners?", body_font, None, 2],
            ["You chose, result", body_font, None, 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(item)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.results_label = play_labels_ref[2]

        # set up artist buttons...
        self.artist_frame = Frame(self.game_frame)
        self.artist_frame.grid(row=3)

        # get the answers from the round artists function
        correct_answer, incorrect_answer = get_round_artists()
        # choose a random artist to print first
        print1 = random.choice([correct_answer, incorrect_answer])
        # if the correct artist is printed first, then print the incorrect answer second
        if print1 == correct_answer:
            print2 = incorrect_answer
        else:
            print2 = correct_answer

        # create the buttons
        self.artist_button = Button(self.artist_frame, font=("Arial", "12"),
                                    text=print1, width=15)
        self.artist_button.grid(row=1,
                                column=1,
                                padx=5, pady=5)

        self.artist_button = Button(self.artist_frame, font=("Arial", "12"),
                                    text=print2, width=15)
        self.artist_button.grid(row=1,
                                column=2,
                                padx=5, pady=5)

        # frame to hold hints and stats button
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # list for buttons (frame | text | bg | command | width | row | colum | text colour)
        control_button_list = [
            [self.game_frame, "Next Round", "#1DB954", "", 21, 5, None, "#FFFFFF"],
            [self.hints_stats_frame, "Hints", "#F9F6F0", "", 10, 0, 0, "#373737"],
            [self.hints_stats_frame, "Stats", "#F9F6F0", "", 10, 0, 1, "#373737"],
            # end button?
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", "16", "bold"),
                                         fg=item[7], width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        def new_round(self):
            """
            Chooses four colours, works out median for score to beat. Configures
            buttons with chosen colours
            """

            # retrieve number of rounds played, add one to it and configure heading
            rounds_played = self.rounds_played.get()
            self.rounds_played.set(rounds_played)

            rounds_wanted = self.rounds_wanted.get()

            # get round colours and median score
            self.round_artist_list, median, highest = get_round_artists()

            # set target score as median (for later comparison)
            self.target_score.set(median)

            # add median and high score to lists for stats
            self.all_high_score_list.append(highest)

            # update heading and score to beat labels. "hide" results label
            self.heading_label.config(text=f"Round {rounds_played + 1} of {rounds_wanted}")
            self.target_label.config(text=f"Target Score: {median}",
                                     font=("Arial", "14", "bold"))
            self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

            # configure buttons using foreground and background colours from list
            # enable colour buttons (disabled at the end of the last round)
            for count, item in enumerate(self.colour_button_ref):
                item.config(fg=self.round_artist_list[count][2], bg=self.round_artist_list[count][0],
                            text=self.round_artist_list[count][0], state=NORMAL)

            self.next_button.config(state=DISABLED)

        def round_results(self, user_choice):
            """
            Retrieves which button was pushed (index 0 - 3), retrieves
            score and then compares it with median, updates results
            and adds results to stats list.
            """
            # enable stats button after at least one round has been played
            self.to_stats_button.config(state=NORMAL)

            # gets user score and colour based on button press...
            score = int(self.round_artist_list[user_choice][1])

            # add one to the number of rounds played and retrieve
            # the number of rounds won
            rounds_played = self.rounds_played.get()
            rounds_played += 1
            self.rounds_played.set(rounds_played)

            rounds_won = self.rounds_won.get()

            # alternative way to get button name. Good for if buttons have been scrambled
            artist_name = self.colour_button_ref[user_choice].cget('text')

            # retrieve target score and compare with user score to find round result
            target = self.target_score.get()

            if score >= target:
                result_text = f"Success! {artist_name} earned you {score} points"
                result_bg = "#82B366"
                self.all_scores_list.append(score)

                rounds_won = self.rounds_won.get()
                rounds_won += 1
                self.rounds_won.set(rounds_won)

            else:
                result_text = f"Oops {artist_name} ({score}) is less than the target. "
                result_bg = "#F8CECC"
                self.all_scores_list.append(0)

            self.results_label.config(text=result_text, bg=result_bg)

            # printing area to generate test data for stats (delete them when done)
            print("all scores", self.all_scores_list)
            print("highest scores:", self.all_high_score_list)

            # enable stats and next buttons, disable colour buttons
            self.next_button.config(state=NORMAL)
            self.to_stats_button.config(state=NORMAL)

            # check to see if game is over
            rounds_wanted = self.rounds_wanted.get()

            # code for when the game ends
            if rounds_played == rounds_wanted:
                # work out success rate
                success_rate = rounds_won / rounds_played * 100
                success_string = ("Success Rate: "
                                  f"{rounds_won} / {rounds_played}"
                                  f"({success_rate:.0f}%")

                # configure end game labels / buttons
                self.heading_label.config(text="Game Over")
                self.target_label.config(text=success_string)
                self.choose_label.config(text="Please click the stats"
                                              " button for more info. ")
                self.next_button.config(state=DISABLED, text="Game Over")
                self.to_stats_button.config(bg="#990000")
                self.end_game_button.config(text="Play Again", bg="#006600"
                                            , compound="right")

            for item in self.colour_button_ref:
                item.config(state=DISABLED)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
