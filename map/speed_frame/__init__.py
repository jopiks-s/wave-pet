import customtkinter as ctk


class SpeedFrame(ctk.CTkFrame):
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(*args, border_width=0, width=width, height=height,
                         **kwargs)

        self.grid_propagate(False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=1)

        # todo: extend slider to slow animation [1, 5] -> [0.1, 5]
        self.speed_slide = ctk.CTkSlider(from_=1, to=5, master=self)
        self.speed_slide.set(1)
        self.speed_lbl = ctk.CTkLabel(text='1x', master=self)

        self.speed_slide.grid(row=0, column=0, sticky='we', padx=(10, 0))  # magic_number
        self.speed_lbl.grid(row=0, column=1, sticky='nsew', padx=(0, 10))
