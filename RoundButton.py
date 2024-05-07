import tkinter as tk

class RoundButton(tk.Canvas):
    def __init__(self, master, text, radius, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.radius = radius
        self.command = command

        self.bind("<Button-1>", self._on_click)

        self._draw_button(text)

    def _draw_button(self, text):
        width = height = 2 * self.radius
        self.config(width=width, height=height)

        self.create_oval(0, 0, width, height, outline="black", fill="red")
        self.create_text(width/2, height/2, text=text, fill="white")

    def _on_click(self, event):
        if self.command:
            self.command()

def on_button_click():
    print("Button clicked")

root = tk.Tk()
root.geometry("200x200")

round_button = RoundButton(root, text="X", radius=20, command=on_button_click)
round_button.pack()

root.mainloop()
