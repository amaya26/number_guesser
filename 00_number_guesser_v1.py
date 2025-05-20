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

    file = open("artists_testing.csv", "r")
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

        # strings for labels
        intro_string = ("In each round you will be invited to choose an artist. Your goal is "
                        "to choose the artist with the most monthly listeners")

        choose_string = "How many rounds do you want to play"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Cool Game Name", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12", "bold"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"]
        ]

        # create labels and add them to the reference list...

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1], fg=item[2],
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label so that it can ne changed to an error message if necessary
        self.choose_label = start_label_ref[2]

        # frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to the home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero"
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # invoke Play class (and take across number of rounds)
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many rounds do you want to play?")
                Play(rounds_wanted)
                # Hide root window (ie: hide rounds choice window)
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

            # display the error if necessary
            if has_errors == "yes":
                self.choose_label.config(text=error, fg="#990099", font=("Arial", "10", "bold"))
                self.num_rounds_entry.config(bg="#F4CCCC")
                self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for playing the Number Guesser game
    """

    def __init__(self, how_many):

        # rounds played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.rounds_won = IntVar()

        # Artist lists and score list
        self.round_artist_list = []
        self.all_scores_list = []
        self.all_high_score_list = []

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

            play_labels_ref.append(self.make_label)

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.results_label = play_labels_ref[2]

        # set up artist buttons...
        self.artist_frame = Frame(self.game_frame)
        self.artist_frame.grid(row=3)

        self.artist_button_ref = []
        self.artist_button_list = []

        # create two buttons in a grid
        for item in range(0, 2):
            self.artist_button = Button(self.artist_frame, font=("Arial", "12"), text="Arist Name",
                                        width=15, command=partial(self.round_results, item))
            self.artist_button.grid(row=item // 2, column=item % 2, pady=5, padx=5)

            self.artist_button_ref.append(self.artist_button)

        # frame to hold hints and stats button
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # list for buttons (frame | text | bg | command | width | row | colum | text colour)
        control_button_list = [
            [self.game_frame, "Next Round", "#1DB954", "", 21, 5, None, "#FFFFFF"],
            [self.hints_stats_frame, "Hints", "#F9F6F0", "", 10, 0, 0, "#373737"],
            [self.hints_stats_frame, "Stats", "#F9F6F0", "", 10, 0, 1, "#373737"],
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", "16", "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.to_help_button = control_ref_list[1]
        self.to_stats_button = control_ref_list[2]

        self.to_stats_button.config(state=DISABLED)

        # once interface has been created, invoke new
        # round function for first round
        self.new_round()

    def new_round(self):
        """
        does something
        """

        # retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()

        rounds_wanted = self.rounds_wanted.get()

        # get round artists and answers
        correct, incorrect = get_round_artists()
        answer_list = [correct, incorrect]
        self.correct_answer = correct

        # update heading label. "hide" results label
        self.heading_label.config(text=f"Round {rounds_played + 1} of {rounds_wanted}")
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        #
        for i in range(2):
            self.artist_button_ref[i].config(text=answer_list[i], state=NORMAL)

        # enable artist buttons (disabled at the end of the last round)
        self.next_button.config(state=DISABLED)

    def round_results(self, user_choice):
        """
        Retrieves which button was pushed (index 0 - 3), retrieves
        score and then compares it with median, updates results
        and adds results to stats list.
        """
        # enable stats button after at least one round has been played
        self.to_stats_button.config(state=NORMAL)

        # add one to the number of rounds played and retrieve
        # the number of rounds won
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_won = self.rounds_won.get()

        # alternative way to get button name. Good for if buttons have been scrambled
        chosen_answer = self.artist_button_ref[user_choice].cget('text')

        if chosen_answer == self.correct_answer:
            result_text = f"Success! {chosen_answer} is correct"
            result_bg = "#82B366"
            self.all_scores_list.append(1)

            rounds_won = self.rounds_won.get()
            rounds_won += 1
            self.rounds_won.set(rounds_won)

        else:
            result_text = f"Oops {chosen_answer} is incorrect. "
            result_bg = "#F8CECC"
            self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # printing area to generate test data for stats (delete them when done)
        print("all scores", self.all_scores_list)
        print("highest scores:", self.all_high_score_list)

        # enable stats and next buttons, disable artist buttons
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
            self.next_button.config(state=DISABLED, text="Game Over")
            self.to_stats_button.config(bg="#990000")

        for item in self.artist_button_ref:
            item.config(state=DISABLED)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Number Guesser")
    StartGame()
    root.mainloop()
