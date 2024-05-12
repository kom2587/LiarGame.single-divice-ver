import tkinter as tk
from random import randint, choice


class LiarGame(tk.Tk):  # Inherit the class Tk into the class LiarGame.
    def __init__(self, title):
        # not fully understood what super() does.
        # Just guessing that it calls "__init__" method of Tk since it doesn't get executed when Tk gets inherited.
        super().__init__()

        # Name the window title
        self.title(title)

        # Draw out all the features on the main window
        self.set_main_window()

        # Draw out all the features on the setting page (which is the first page)
        self.set_setting_page()

        self.mainloop()

    # Draw out all the features on the main window
    def set_main_window(self):
        # Create pages as a dictionary
        self.pages = {"setting": None, "main": None, "list": None}
        for page_name in self.pages:
            self.pages[page_name] = self.create_widget(self, tk.Frame, pack=False)

        # Create a rule description button on the main window
        self.rule_btn = self.create_widget(self, tk.Button, text="How To Play", command=self.show_rule, side="top",
                                           anchor="nw")

        # Create a quitting button on the main window
        def quit_warning():
            quit_warning_window = self.create_sub_window("Are you sure you want to quit the game?", yes_btn_command=self.destroy, back_btn_usage=True)
        self.quit_btn = self.create_widget(self, tk.Button, text="Quit", command=quit_warning, side="bottom",
                                           anchor="sw")

    # Create the rule description sub window
    def show_rule(self):
        with open("rule_description.txt", "r") as file:
            rule = file.read()
            rule_window = self.create_sub_window()
            rule_text = self.create_widget(rule_window, tk.Text, wrap="word")
            rule_text.insert(tk.END, rule)
            rule_text.config(state="disabled")
            # Can't use the "back_btn_usage" argument of the "create_sub_window" method because the btn goes to the top of the window
            rw_back_btn = self.create_widget(rule_window, tk.Button, text="Back", command=rule_window.destroy)

            # Just add it because the sub window doesn't automatically fit into the screen in Android.
            self.fit_window(rule_window)

    # Common method for resizing a window when it's larger than the screen (Doesn't exclude the taskbar. Need to be fixed.)
    def fit_window(self, window, padding=30):
        self.update()
        screen_width = self.winfo_screenwidth() - padding
        screen_height = self.winfo_screenheight() - padding
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        if screen_width < window_width:
            window.geometry(f"{screen_width}x{window_height}")
        if screen_height < window_height:
            window.geometry(f"{window_width}x{screen_height}")

    # Common method for switching between pages.
    def show_page(self, page):
        if self.cur_page:
            self.cur_page.pack_forget()
        page.pack(fill="both", expand=True)
        self.cur_page = page

    # Common method for create various kinds of widgets
    def create_widget(self, parent, widget_type, text=None, command=None, wrap=None, pack=True, side=None, anchor=None):
        widget = widget_type(parent, text=text, command=command, wrap=wrap)
        if pack:
            widget.pack(side=side, anchor=anchor)
        return widget

    # Common method for create a listbox
    def create_listbox(self, parent, items):
        listbox = self.create_widget(parent, tk.Listbox)
        for element in items:
            listbox.insert(tk.END, element)
        return listbox

    # Common method for create a sub window
    def create_sub_window(self, label_text=None, yes_btn_command=None, back_btn_usage=False):
        sub_window = tk.Toplevel(self)
        if label_text:
            label = self.create_widget(sub_window, tk.Label, text=label_text)
        if back_btn_usage:
            back_button = self.create_widget(sub_window, tk.Button, text="Back", command=sub_window.destroy)
        if yes_btn_command:
            yes_button = self.create_widget(sub_window, tk.Button,text="Yes", command=yes_btn_command)
        return sub_window

    # Common method for delete all the widgets in a widget
    def del_widgets(self, page):
        for widget in page.winfo_children():
            widget.destroy()

    # Load word bank from a txt file.
    def load_word_bank(self, file_path):
        with open(file_path, "r") as file:
            word_bank = [line.strip() for line in file]
        return word_bank

    # Draw out all the features on the setting page (which is the first page)
    def set_setting_page(self):
        # Show the setting page initially
        self.cur_page = None
        self.show_page(self.pages["setting"])

        # Create widgets on the setting page
        player_entry_label = self.create_widget(self.pages["setting"], tk.Label, text="Enter number of players:")
        self.player_entry = self.create_widget(self.pages["setting"], tk.Entry)
        start_button = self.create_widget(self.pages["setting"], tk.Button, text="Start Game!", command=self.start_game)

    # Initialize the game when the user starts it.
    def start_game(self):
        # Check if the value the user gave is natural number.
        if not self.player_entry.get().isdigit() or int(self.player_entry.get()) == 0:
            alart_window = self.create_sub_window("Please enter a natural number", back_btn_usage=True)
            return
        else:
            # Set up the background settings.
            self.word_bank = self.load_word_bank("word_bank.txt")
            self.answer = choice(self.word_bank)
            num_players = int(self.player_entry.get())
            player_list = ['Player ' + str(i) for i in range(1, num_players + 1)]
            self.liar_index = randint(0, num_players - 1)

            # Set up the main page.
            self.player_listbox = self.create_listbox(self.pages["main"], player_list)
            show_answer_btn = self.create_widget(self.pages["main"], tk.Button, text="Show selected player's answer",
                                                 command=self.selection_check)
            self.create_widget(self.pages["main"], tk.Button, text="Show word bank",
                                                    command=lambda: self.show_page(self.pages["list"]))
            new_game_btn = self.create_widget(self.pages["main"], tk.Button, text="New game", command=self.new_game,
                                              side="bottom", anchor="s")

            # Set up the list page
            word_listbox = self.create_listbox(self.pages["list"], self.word_bank)
            back_button = self.create_widget(self.pages["list"], tk.Button, text="Go back",
                                             command=lambda: self.show_page(self.pages["main"]))

            self.show_page(self.pages["main"])

    # Check if the user is ready to see the answer before showing it
    def selection_check(self):
        if self.player_listbox.curselection():
            self.selected_index = self.player_listbox.curselection()[0]
            check_window = self.create_sub_window(
                f"Are you sure you are {self.player_listbox.get(self.selected_index)}?", yes_btn_command=lambda: (check_window.destroy(), self.show_answer()), back_btn_usage=True)
        else:
            return  # Nothing happens when there is no selection.

    # Show the answer with a countdown
    def show_answer(self):
        # Check whether the player is the liar or not.
        prompt = ""
        if self.selected_index == self.liar_index:
            prompt = "You are the liar!!!"
        else:
            prompt = f"The word is <{self.answer}>"

        # Create the sub window
        answer_window = self.create_sub_window(prompt, back_btn_usage=True)
        aw_back_btn = self.create_widget(answer_window, tk.Button, command=answer_window.destroy)

        # Close the sub window automatically
        def countdown(remaining_sec):
            aw_back_btn.config(text=f"Go back ({remaining_sec})")
            if remaining_sec > 0:
                answer_window.after(1000, lambda: (countdown(remaining_sec-1)))  # I can't fully understand what happens when "answer_window" get closed while "after" method is being executed.
            else:
                answer_window.destroy()
        countdown(remaining_sec=5)

    # Start a new game
    def new_game(self):
        # delete all the widgets in the main and list pages.
        for del_pg_name in ("main", "list"):
            self.del_widgets(self.pages[del_pg_name])

        # Come back to the setting page.
        self.show_page(self.pages["setting"])


LiarGame("Liar Game")
