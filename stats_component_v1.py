from tkinter import *
from functools import partial  # to prevent unwanted windows


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

        # Strings for labels
        intro_string = ("In each round you will be invited to choose a colour."
                        "Your goal is to beat the target score and win the round "
                        "(and keep your points).")
        # choose_string = "Oops - Please choose a whole number more than zero."
        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Colour Quest", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"]
        ]

        # create labels and add them to the reference list

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2],
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label so that it can be changed to an
        # error message if necessary
        self.choose_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=20)
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

        # Retrieve temperature to be converted
        rounds_wanted = 5
        self.to_play(rounds_wanted)

    def to_play(self, num_rounds):
        """
        Invokes game GUI and takes across number of rounds to be played
        """
        Play(num_rounds)
        # hide root window (ie: hide rounds choice window)
        root.withdraw()


class Play:
    """
    Interface for playing the Colour Quest game
    """

    def __init__(self, how_many):
        self.rounds_won = IntVar()

        # lists for stats component

        # highest score test data
        # self.all_scores_list = [20, 20, 20, 16, 19]
        # self.all_high_score_list = [20, 20, 20, 16, 19]
        # self.rounds_won.set(5)

        # lowest score test data
        # self.all_scores_list = [0, 0, 0, 0, 0]
        # self.all_high_score_list = [20, 20, 20, 16, 19]
        # self.rounds_won.set(0)

        # random score test data
        self.all_scores_list = [0, 15, 16, 0, 16]
        self.all_high_score_list = [20, 19, 18, 20, 20]
        self.rounds_won.set(3)

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Number Guesser",
                                   font=("Arial", "16", "bold"), pady=5, padx=5)
        self.heading_label.grid(row=0)

        self.stats_button = Button(self.game_frame, text="Stats",
                                     font=("Arial", "14", "bold"),
                                     fg="#FFFFFF", bg="#373737", width=15,
                                     padx=10, pady=10,
                                     command=self.to_stats)
        self.stats_button.grid(row=1)

    def to_stats(self):
        """
        retrieves everything we need to display the game
        """

        # important: retrieve number of rounds
        # won as a number (rather than the 'self' container)
        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won, self.all_scores_list,
                        self.all_high_score_list]

        Stats(self, stats_bundle)


class Stats:

    def __init__(self, partner, all_stats_info):
        print("Displays the stats window")

        # extract information from the master list
        rounds_won = all_stats_info[0]
        user_scores = all_stats_info[1]

        # sort user score to find high score...
        user_scores.sort()

        # setup dialogue box
        self.stats_box = Toplevel()

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        # if user press cross at top, close stats and 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300, height=200)
        self.stats_frame.grid()

        # math to populate stats dialogue
        rounds_played = len(user_scores)

        success_rate = rounds_won / rounds_played * 100
        total_score = sum(user_scores)

        # strings for start labels

        success_string = (f"Success Rate: {rounds_won} / {rounds_played} "
                          f"({success_rate:.0f}%)")
        total_score_string = f"Total Score: {total_score}"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")

        # Label list (text | font | 'Sticky')
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left", padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        self.dismiss_button = Button(self.stats_frame, font=("Arial", "16", "bold"),
                                     text="Dismiss", bg="#333333", fg="#FFFFFF", width=20,
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

    def close_stats(self, partner):
        print("Closes the stats window")
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Number Guesser")
    StartGame()
    root.mainloop()
