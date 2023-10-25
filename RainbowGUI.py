import tkinter as tk
from tkinter import colorchooser
import random
from Rainbow import Rainbow
import json


class RainbowGUI:
    def __init__(self):
        # parameters

        # application
        self.app_title = "Stakeholder Rainbow Diagram Builder"
        # spacing
        self.padding_x = 1
        self.padding_y = 1
        # sliders
        self.slider_min = 0
        self.slider_max = 100
        self.slider_default = 50
        # columns
        self.column_titles = [
            ("Stakeholder", "A person, group, or entity who can affect, or could be affected by your project."),
            ("Influence", "How much power / authority this stakeholder has over your project."),
            ("Affected", "How much impact will your project have on this stakeholder."),
            ("Colour", "Colour of the stakeholder's dot. Keep unique for clarity."),
        ]
        # add stakeholder button
        self.stakeholder_button_name = "Add Stakeholder"
        # build diagram button
        self.build_button_name = "Build Diagram"
        # colour button
        self.colour_button_name = " "
        
        # variables built later
        self.app = None
        self.add_button = None
        self.build_button = None
        self.entry_labels = None
        
        
    def generate_random_color(self):
        # Generate a random color in hexadecimal format
        color = "#{:02X}{:02X}{:02X}".format(random.randint(
            0, 255), random.randint(0, 255), random.randint(0, 255))
        return color


    def add_entry_label(self):

        # stakeholder name input
        new_label = tk.Entry(self.app)
        new_label.grid(row=len(self.entry_labels) + 2, column=0,
                    padx=self.padding_x, pady=self.padding_y)

        # influence slider
        slider1 = tk.Scale(self.app, from_=self.slider_min,
                        to=self.slider_max, orient="horizontal")
        slider1.set(self.slider_default)
        slider1.grid(row=len(self.entry_labels) + 2, column=1,
                    padx=self.padding_x, pady=self.padding_y)

        # affected slider
        slider2 = tk.Scale(self.app, from_=self.slider_min,
                        to=self.slider_max, orient="horizontal")
        slider2.set(self.slider_default)
        slider2.grid(row=len(self.entry_labels) + 2, column=2,
                    padx=self.padding_x, pady=self.padding_y)

        # colour changer button
        color_button = tk.Button(self.app, text=self.colour_button_name,
                                command=lambda label=new_label: self.pick_color(label))
        random_color = self.generate_random_color()
        color_button.configure(bg=random_color, width=3, height=1)
        color_button.grid(row=len(self.entry_labels) + 2, column=3,
                        padx=self.padding_x, pady=self.padding_y)

        # remove stakeholder button
        remove_button = tk.Button(self.app, text="Remove", fg="red",
                                command=lambda label=new_label: self.remove_entry_label(label))
        remove_button.grid(row=len(self.entry_labels) + 2,
                        column=4, padx=self.padding_x, pady=self.padding_y)

        self.entry_labels.append((new_label, slider1, slider2,
                            color_button, remove_button))

        # add new stakeholder row button
        self.add_button.grid(row=len(self.entry_labels) + 3, column=0,
                        padx=self.padding_x, pady=self.padding_y)


    def pick_color(self, label):
        color = colorchooser.askcolor()[1]
        for entry_label, _, _, color_button, _ in self.entry_labels:
            if entry_label == label:
                #entry_label.configure(fg=color)
                color_button.configure(bg=color)


    def remove_entry_label(self, label):
        for entry_label, slider1, slider2, color_button, button in self.entry_labels:
            if entry_label == label:
                entry_label.grid_forget()
                slider1.grid_forget()
                slider2.grid_forget()
                color_button.grid_forget()
                button.grid_forget()
                self.entry_labels.remove(
                    (entry_label, slider1, slider2, color_button, button))

        for i, (entry_label, slider1, slider2, color_button, remove_button) in enumerate(self.entry_labels):
            entry_label.grid(row=i + 2, column=0, padx=self.padding_x, pady=self.padding_y)
            slider1.grid(row=i + 2, column=1, padx=self.padding_x, pady=self.padding_y)
            slider2.grid(row=i + 2, column=2, padx=self.padding_x, pady=self.padding_y)
            color_button.grid(row=i + 2, column=3, padx=self.padding_x, pady=self.padding_y)
            remove_button.grid(row=i + 2, column=4, padx=self.padding_x, pady=self.padding_y)

        # Move the "Add Entry Label" button to the bottom of the list
        self.add_button.grid(row=len(self.entry_labels) + 3, column=0,
                        padx=self.padding_x, pady=self.padding_y)


    def build_diagram(self):
        stakeholders = []
        for entry_label, slider1, slider2, color_button, _ in self.entry_labels:
            label_name = entry_label.get()
            slider_value1 = slider1.get() / 100
            slider_value2 = slider2.get() / 100
            color = color_button.cget("bg")
            stakeholders.append(
                (label_name, slider_value1, slider_value2, color))

        
        self.app.destroy()
        self.save_data(stakeholders)
        print(stakeholders)

        r = Rainbow(stakeholders)
        r.build()

    def run_app(self):
        # application

        self.app = tk.Tk()
        self.app.title(self.app_title)

        # columns titles
        for idx, pair in enumerate(self.column_titles):
            title, tooltip = pair
            temp_label = tk.Label(self.app, text=title)
            temp_label.grid(row=1, column=idx, padx=self.padding_x, pady=self.padding_y)
            self.add_tooltip(temp_label, tooltip)

        self.entry_labels = []
        
        # add stakeholder button
        self.add_button = tk.Button(self.app, text=self.stakeholder_button_name, command=self.add_entry_label)
        self.add_button.grid(row=2, column=0, padx=self.padding_x, pady=self.padding_y)

        # build button
        self.build_button = tk.Button(self.app, text=self.build_button_name, command=self.build_diagram)
        self.build_button.grid(row=0, column=3, padx=self.padding_x, pady=self.padding_y)

        self.load_saved_data()
        
        self.app.mainloop()
        
    def add_tooltip(self, element, text):
        ToolTip(element, text)
    
    def save_data(self, data):
        with open("data.json", "w") as f:
            json.dump(data, f)


    def load_data(self):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return []


    def load_saved_data(self):
        data = self.load_data()
        
        if len(data) < 1:
            return
        
        for item in data:
            self.add_entry_label()
            entry_label, slider1, slider2, color_button, _ = self.entry_labels[-1]
            entry_label.delete(0, tk.END)
            entry_label.insert(0, item[0])
            slider1.set(item[1] * 100)
            slider2.set(item[2] * 100)
            color_button.configure(bg=item[3])


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text,
                         background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None







if __name__ == "__main__":
    
    r = RainbowGUI()
    r.run_app()
