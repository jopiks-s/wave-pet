from tkinter import Misc


def on_complete_impulse_animation(root: Misc, flash_number: int, flash_speed: int, flash_rate: int, border_color: str):
    from . import BoardFrame
    root: BoardFrame

    def __inner__(flash_counter: int, up: bool):
        nonlocal flash_number, flash_speed, flash_rate, root, memorize_color

        if flash_counter < flash_number:
            curr_border_width = root.cget('border_width')
            max_border_width = root.border_width
            if up:
                if curr_border_width + 1 > max_border_width:
                    root.after(flash_rate, __inner__, flash_counter, False)
                else:
                    root.configure(border_width=curr_border_width + 1)
                    root.after(flash_speed, __inner__, flash_counter, True)
            else:
                if curr_border_width - 1 < 0:
                    root.after(flash_rate, __inner__, flash_counter + 1, True)
                else:
                    root.configure(border_width=curr_border_width - 1)
                    root.after(flash_speed, __inner__, flash_counter, False)
        else:
            root.configure(border_color=memorize_color, border_width=0)

    memorize_color = root.cget('border_color')
    root.configure(border_color=border_color)
    __inner__(0, True)


def _on_complete_change(self, var, index, mode):
    from . import BoardFrame
    self: BoardFrame

    if self.board.complete.get():
        on_complete_impulse_animation(self, 2, 30, 100, 'green')
    else:
        on_complete_impulse_animation(self, 1, 60, 0, 'gray')

