# pylint: disable=W0601
# pylint: disable=W0603
# pylint: disable=C0103
"""
Modul progress bar
"""
from tkinter import Toplevel, Label, DoubleVar
from tkinter.ttk import Progressbar


class ProgressBar:
    """
    The class that runs the progress bar
    """
    def start(self):
        """
        starts the progress bar
        """
        global popup
        global progress_var
        global progress
        popup = Toplevel()
        Label(popup, text="Files being converting").grid(row=0, column=0)
        popup.geometry('100x100+100+450')
        progress = 0
        progress_var = DoubleVar()
        progress_bar = Progressbar(popup, variable=progress_var, maximum=100)
        progress_bar.grid(row=1, column=0)  # .pack(fill=tk.X, expand=1, side=tk.BOTTOM)
        self.center(popup)

        popup.pack_slaves()

    @staticmethod
    def update_progress(progress_step):
        """
        updates progress bar
        :param progress_step: step of progress
        """
        popup.update()
        global progress
        progress += progress_step
        progress_var.set(progress)

    @staticmethod
    def exit_progress():
        """
        exit progress bar
        """
        popup.destroy()
        popup.update()

    @staticmethod
    def center(win):
        """
        centers a tkinter window
        :param win: the root or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()
