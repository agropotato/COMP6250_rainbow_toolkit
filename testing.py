import tkinter as tk
from ttkthemes import ThemedTk
from ttkthemes import ThemedStyle
from tkinter import ttk

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

        label = tk.Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def create_tooltip(label, text):
    ToolTip(label, text)

# Create the main window
root = ThemedTk(theme="arc")
style = ThemedStyle(root)
style.set_theme("plastik")  # You can change the theme to one of your choice

root.title("Label Tooltip Example")
root.geometry("300x200")

# Create a label with a tooltip
label = ttk.Label(root, text="Hover over me for a tooltip")
label.pack(pady=20)
create_tooltip(label, "This is a tooltip.")

root.mainloop()