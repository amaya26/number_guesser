from tkinter import *
from functools import partial # to prevent unwanted windows


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

        # set up colour buttons...
        self.artist_frame = Frame(self.game_frame)
        self.artist_frame.grid(row=3)

        # create four buttons in a 2 x 2 grid
        for item in range(0, 2):
            self.artist_button = Button(self.artist_frame, font=("Arial", "12"),
                                        text="Artist Name", width=15)
            self.artist_button.grid(row=item // 2,
                                    column=item % 2,
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


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
