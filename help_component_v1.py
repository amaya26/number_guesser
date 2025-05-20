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
            ["Number Guesser", ("Arial", "16", "bold"), None],
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
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Number Guesser",
                                   font=("Arial", "16", "bold"), pady=5, padx=5)
        self.heading_label.grid(row=0)

        self.to_help_button = Button(self.game_frame, text="Hints",
                                     font=("Arial", "14", "bold"),
                                     fg="#FFFFFF", bg="#373737", width=15,
                                     padx=10, pady=10,
                                     command=self.to_hints)
        self.to_help_button.grid(row=1)

    def to_hints(self):
        """
        Displays hints for playing the game
        :return:
        """
        DisplayHints(self)


class DisplayHints:
    """
    Displays hints for Colour quest game
    """

    def __init__(self, partner):
        print("Hints window appears")
        # setup dialogue box and background colour
        background = "#E7E7E7"
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_button.config(state=DISABLED)

        # if user press cross at top, close help and 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame, text="\nHints",
                                        font=("Arial", "16", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "\nThis game involves choosing between two artists. Click the one with the highest " \
                    "monthly listeners on Spotify. If you're correct, you'll earn a point. Click the Stats " \
                    "button to view your score. The game will end once you've played the number of rounds entered " \
                    "at the start. Good luck! \n"

        self.help_text_label = Label(self.help_frame, text=help_text,
                                     wraplength=350, justify="left", font=("Arial", "12"))
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame, font=("Arial", "14", "bold"),
                                     text="Dismiss", bg="#1db954", fg="#FFFFFF", command=partial(self.close_help,
                                                                                                 partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set the background colour on everything except the buttons
        recolour_list = [self.help_frame, self.help_heading_label, self.help_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        print("Closes Hints window")
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
