
from tkinter import *


# classes start here
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
        intro_string = ("In each round you will be shown two artists. Click on"
                        " the one with the most monthly listeners to gain a "
                        "point.")
        # choose_string = "Oops - Please choose a whole number more than zero."
        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Cool Game Name", ("Arial", "16", "bold"), "#373737"],
            [intro_string, ("Arial", "12"), "#373737"],
            [choose_string, ("Arial", "12", "bold"), "#373737"]
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
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#f9f6f0", bg="#1db954", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieve temperature to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users want to come back to home screen)
        self.choose_label.config(fg="#373737", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please type in a whole number more than zero."
        has_errors = "no"

        # Checks that the amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if 0 < rounds_wanted < 101:
                # clear entry box and reset instruction label so that when users
                # play a new game, they don't see and error message
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many rounds do you want to play?")

                # for testing purposes
                print(f"Program continues - {rounds_wanted}")
                self.choose_label.config(text="Closes window and opens the game interface. ")
                # Invoke Play Class (and take across number of rounds)
                # Hide root window (ie hide rounds choice window)
                # root.withdraw()
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            print(f"Error - {rounds_wanted}")
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", "10", "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
