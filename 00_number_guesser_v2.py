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

        self.start_frame = Frame(padx=10, pady=10, bg="#e7e7e7")
        self.start_frame.grid()

        # strings for labels
        intro_string = ("In each round you will be invited to choose a colour. your goal is "
                        "to beat the target score and win the round (and keep your points)")

        # choose string = "Oops - Please choose a whole number more than zero."
        choose_string = "How many rounds do you want to play"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Colour Quest", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12", "bold"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"]
        ]

        # create labels and add them to the reference list...

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1], fg=item[2], bg="#e7e7e7",
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label so that it can ne changed to an error message if necessary
        self.choose_label = start_label_ref[2]

        # frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame, bg="#e7e7e7")
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
        self.num_rounds_entry.config(bg="#e7e7e7")

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
    Interface for playing the Colour Quest game
    """

    def __init__(self, how_many):

        # rounds played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.rounds_won = IntVar()

        # colour lists and score list
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
                                    bg="#e7e7e7", wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # retrieve labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.choose_label = play_labels_ref[2]
        self.results_label = play_labels_ref[2]

        # set up artist buttons...
        self.artist_frame = Frame(self.game_frame)
        self.artist_frame.grid(row=3)

        self.artist_button_ref = []
        self.artist_button_list = []

        # create two buttons in a grid
        for item in range(0, 2):
            self.artist_button = Button(self.artist_frame, font=("Arial", "12"), text="Colour Name",
                                        width=15, command=partial(self.round_results, item))
            self.artist_button.grid(row=item // 2, column=item % 2, pady=5, padx=5)

            self.artist_button_ref.append(self.artist_button)

        # frame to hold hints and stats button
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # list for buttons (frame | text | bg | command | width | row | column
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", self.new_round, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", self.to_hints, 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", self.to_stats, 10, 0, 1],
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
        button1 = random.choice(answer_list)
        if button1 == correct:
            button2 = incorrect
        else:
            button2 = correct

        self.correct_answer = correct

        # update heading label. "hide" results label
        self.heading_label.config(text=f"Round {rounds_played + 1} of {rounds_wanted}")
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        self.artist_button_ref[0].config(text=button1, state=NORMAL)
        self.artist_button_ref[1].config(text=button2, state=NORMAL)

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
        print(chosen_answer)

        if chosen_answer == self.correct_answer:
            result_text = f"Success! {chosen_answer} is correct"
            result_bg = "#82B366"
            # change it pleaseeeeee!!!!!!!!!! #IUFABGILUEABROU
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

        # enable stats and next buttons, disable colour buttons
        self.next_button.config(state=NORMAL)
        self.to_stats_button.config(state=NORMAL)

        # check to see if game is over
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            # work out success rate
            success_rate = rounds_won / rounds_played * 100
            success_string = (f"Success Rate: "
                              f"{rounds_won} / {rounds_played}"
                              f"({success_rate:.0f}%)")
            # configure 'end game' labels / buttons
            self.heading_label.config(text="Game Over")
            self.target_label.config(text=success_string)
            self.choose_label.config(text="Please click the stats button for more info")
            self.next_button.config(state=DISABLED, text="Game Over")
            self.to_stats_button.config(bg="#990000")

        for item in self.artist_button_ref:
            item.config(state=DISABLED)

    def close_play(self):
        # reshow root (ie: close rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_hints(self):
        """
        displays hints for playing game
        :return:
        """
        DisplayHints(self)

    def to_stats(self):
        """
        displays hints for playing game
        """
        # important: retrieve number of rounds
        # won as a number (rather than the self container
        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won, self.all_scores_list, self.all_high_score_list]

        Stats(self, stats_bundle)

class Stats:

    """
    Temperature conversion tool
    """

    def __init__(self, partner, all_stats_info):

        # extract information from the master list
        rounds_won = all_stats_info[0]
        user_scores = all_stats_info[1]
        high_scores = all_stats_info[2]

        # sort user score to find high score...
        user_scores.sort()

        # setup dialogue box
        self.stats_box = Toplevel()

        # disable stats button
        partner.to_stats_button.config(state=DISABLED)

        # if user press cross at top, close stats and 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300, height=200)
        self.stats_frame.grid()

        # math to populate stats dialogue
        rounds_played = len(user_scores)

        success_rate = rounds_won / rounds_played * 100
        total_score = sum(user_scores)
        max_possible = sum(high_scores)

        best_score = user_scores[-1]
        average_score = total_score / rounds_played

        # strings for start labels

        success_string = (f"Success Rate: {rounds_won} / {rounds_played}"
                          f"({success_rate:.0f}%)")
        total_score_string = f"Total Score: {total_score}"
        max_possible_string = f"Maximum Possible Score: {max_possible}"
        best_score_string = f"Best Score: {best_score}"

        # custom comment text and formatting
        if total_score == max_possible:
            comment_string = "Amazing! You got the highest possible score!"
            comment_colour = "#D5E8D4"

        elif total_score == 0:
            comment_string = "Oops - You lose every round! You might want to look at the hints"
            comment_colour = "#F8CECC"

        else:
            comment_string = ""
            comment_colour = "#F0F0F0"

        average_score_string = f"Average Score: {average_score:.0f}\n"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("Arial", "13")

        # Label list (text | font | 'Sticky')
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
            [max_possible_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
            ["\nRound Stats", heading_font, ""],
            [best_score_string, normal_font, "W"],
            [average_score_string, normal_font, "W"]
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left", padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # configure comment label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[4]
        stats_comment_label.config(bg=comment_colour)

        self.dismiss_button = Button(self.stats_frame, font=("Arial", "16", "bold"),
                                     text="Dismiss", bg="#333333", fg="#FFFFFF", width=20,
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

    def close_stats(self, partner):
        partner.to_stats_button.config(state=NORMAL)
        self.stats_box.destroy()

class DisplayHints:

    """
    Temperature connversion tool
    """

    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_button.config(state=DISABLED)

        # if user press cross at top, close help and 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200)
        self.help_frame.grid()

        self.help_hearing_label = Label(self.help_frame, text="Help / Info",
                                        font=("Arial", "14", "bold"))
        self.help_hearing_label.grid(row=0)

        help_text = "To use the program, simply enter the temperature you wish to convert and then choose" \
                    "to convert to either degrees Celsius (centigrade) or Fahrenheit... \n\n" \
                    "Note that -273 degrees C (-459 F) is absolute zero (the coldest possible temperature)." \
                    "If you try to convert a temperature that is less than -273 degrees C, you will get an" \
                    "error message. To see your calculation history and export it to a text file, please" \
                    "click the 'History / Export' button."

        self.help_text_label = Label(self.help_frame, text=help_text,
                                     wraplength=350, justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame, font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600", fg="#FFFFFF", command=partial(self.close_help,
                                                                                                 partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set the background colour on everything except the buttons
        recolour_list = [self.help_frame, self.help_hearing_label, self.help_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()