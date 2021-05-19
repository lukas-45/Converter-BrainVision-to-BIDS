# pylint: disable=W0601
# pylint: disable=W0603
# pylint: disable=C0103
"""
Module that takes care of the gui
"""
import glob
import os
import threading
import shutil
from tkinter import Tk, BOTH, W, N, E, S, Radiobutton, \
    messagebox, Entry, Scrollbar, Listbox, IntVar, StringVar
from tkinter.ttk import Frame, Button, Label, Separator
from tkinter import filedialog
import brain_vision_converter
import metadata_transform
import progress_bar
from tkinter import ttk
import re
import logging

ID_GUI = 1


class GUI(Frame):
    """
    GUI class
    """
    def __init__(self):
        super().__init__()
        self.text = StringVar()
        self.text.set("Dataset directory path")
        self.init_ui()

    def init_ui(self):
        """
        sets the appearance of the window
        """
        global data_dir_label
        global exp_dir_label
        global exp_tar_label
        global data_tar_label
        global label_dir
        global lb
        global entry

        global exp_dir_button
        global exp_tar_button

        global data_dir_button
        global data_tar_button

        global transfer_button

        global radiobutton_data
        global radiobutton_experiment

        global delete_button
        global clear_button

        global vhd_r_files
        vhd_r_files = []

        self.master.title("LukkoBids")
        self.master.configure(background='#094064')
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(6, pad=10)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, pad=8)

        sep = Separator(self, orient="vertical")
        sep1 = Separator(self, orient="vertical")
        sep2 = Separator(self, orient="vertical")
        sep3 = Separator(self, orient="vertical")
        sep.grid(column=2, row=0, sticky="ns")
        sep1.grid(column=2, row=1, sticky="ns")
        sep2.grid(column=2, row=2, sticky="ns")
        sep3.grid(column=2, row=3, sticky="ns")

        seph = Separator(self, orient="horizontal")
        sep1h = Separator(self, orient="horizontal")
        sep2h = Separator(self, orient="horizontal")
        sep3h = Separator(self, orient="horizontal")
        sep4h = Separator(self, orient="horizontal")
        seph.grid(column=0, row=4, sticky="ew")
        sep1h.grid(column=1, row=4, sticky="ew")
        sep2h.grid(column=2, row=4, sticky="ew")
        sep3h.grid(column=3, row=4, sticky="ew")
        sep4h.grid(column=4, row=4, sticky="ew")

        style = ttk.Style()
        style.theme_use('alt')
        style.configure(self.master, background='#2A6C93')
        style.configure('TButton', font=('Georgia', 8), background='#14577E', foreground='white')
        style.map('TButton', background=[('active', '#437CA1')])
        style.configure('TLabel', font=('Georgia', 8), foreground='white')

        label_dir = Label(self, textvariable=self.text, wraplength=550)

        label_dir.grid(row=5, columnspan=5)

        exp_dir_button = Button(self, text="Experiment input", command=self.clicked_choose_input, width=14)
        exp_dir_button.grid(row=2, column=3)
        exp_dir_label = Label(self, text="Original experiment location", wraplength=200)
        exp_dir_label.grid(row=2, column=4, padx=5)

        exp_tar_button = Button(self, text="Experiment output", command=self.clicked_choose_target, width=14)
        exp_tar_button.grid(row=3, column=3, pady=4)
        exp_tar_label = Label(self, text="Converted experiment location", wraplength=200)
        exp_tar_label.grid(row=3, column=4, padx=5)

        data_dir_button = Button(self, text="Dataset input", command=self.clicked_choose_input, width=11)
        data_dir_button.grid(row=2, column=0)
        data_dir_label = Label(self, text="Original dataset location", wraplength=200)
        data_dir_label.grid(row=2, column=1, padx=5)

        data_tar_button = Button(self, text="Dataset output", command=self.clicked_choose_target, width=11)
        data_tar_button.grid(row=3, column=0, pady=4)
        data_tar_label = Label(self, text="Converted dataset location", wraplength=200)
        data_tar_label.grid(row=3, column=1)

        data_name_label = Label(self, text="Dataset name: ")
        data_name_label.grid(row=1, column=0, padx=5)

        entry = Entry(self)
        entry.grid(row=1, column=1, pady=6)

        transfer_button = Button(self, text="Convert data", command=self.clicked_conversion_button, width=11)
        transfer_button.grid(row=6, padx=5, columnspan=6)

        scrollbar = Scrollbar(self, orient="vertical")
        lb = Listbox(self, yscrollcommand=scrollbar.set)
        scrollbar.config(command=lb.yview)

        lb.grid(row=7, column=0, columnspan=5, rowspan=1,
                padx=5, sticky=E+W+S+N)

        radiobutton_data = Radiobutton(self,
                                       text="ADD dataset",
                                       padx=20,
                                       variable=v,
                                       command=self.show_choice,
                                       value=1)
        radiobutton_experiment = Radiobutton(self,
                                             text="ADD experiment to existing dataset",
                                             padx=20,
                                             variable=v,
                                             command=self.show_choice,
                                             value=2,
                                             wraplength=105)
        radiobutton_data.grid(row=0, column=0)
        radiobutton_experiment.grid(row=0, column=3)

        radiobutton_data.configure(font=('Georgia', 8), fg="white", bg='#2A6C93', activebackground='#2A6C93',
                                   activeforeground="white", selectcolor='#2A6C93')
        radiobutton_experiment.configure(font=('Georgia', 8), fg="white", bg='#2A6C93', activebackground='#2A6C93',
                                         activeforeground="white", selectcolor='#2A6C93')

        delete_button = Button(self, text="Clear exp", command=self.delete_item, width=11)
        clear_button = Button(self, text="Clear all", command=self.clear_list, width=11)
        delete_button.grid(row=8, column=0)
        clear_button.grid(row=8, column=4)

        self.show_choice()

    def show_choice(self):
        """
        sets the visibility of the buttons
         according to the radio buttons
        """
        if v.get() == 1:
            exp_dir_button.config(state="disable")
            exp_tar_button.config(state="disable")
            data_dir_button.config(state="normal")
            data_tar_button.config(state="normal")
            self.clear_list()
            self.text.set("Directory dataset path")
        if v.get() == 2:
            exp_dir_button.config(state="normal")
            exp_tar_button.config(state="normal")
            data_dir_button.config(state="disable")
            data_tar_button.config(state="disable")
            self.clear_list()
            self.text.set("Directory experiment path")

    @staticmethod
    def next_id():
        """
        counter id
        """
        global ID_GUI
        ID_GUI += 1
        res = ID_GUI
        return res

    def clicked_conversion_button(self):
        """
        disable buttons and then start new thread
        which start transform data
        """
        self.disable_buttons()
        threading.Thread(target=self.get_conversion_data).start()

    def get_conversion_data(self):
        index = 0
        try:
            if v.get() == 1:
                metadata_transform.MetadataConvert().create_meta_data_file()
            if v.get() == 2:
                shutil.copy(os.path.join(target_dir, 'participants.tsv'), os.path.join('./', 'participants.tsv'))

            progress_bar.ProgressBar().start()
            progress_step = float(100.0 / lb.size())
            for vhd_r_file in list(vhd_r_files):
                progress_bar.ProgressBar().update_progress(progress_step)
                if v.get() == 1:
                    if index == 0:
                        brain_vision_converter.IID = 1
                    brain_vision_converter.BrainVisionConverter()\
                        .convert_data_to_bids(vhd_r_file,
                                              entry.get(), target_dir, xml_files)
                elif v.get() == 2:
                    brain_vision_converter.BrainVisionConverter().\
                        get_id(target_dir)
                    brain_vision_converter.BrainVisionConverter().\
                        convert_data_to_bids_experiment(vhd_r_file,
                                                        target_dir)
                index = index+1

            progress_bar.ProgressBar().exit_progress()
            if v.get() == 1:
                shutil.move(os.path.join('./', 'participants.tsv'),
                            os.path.join(target_dir + '/' + entry.get(),
                                         'participants.tsv'))
                if len(xml_files) > 0:
                    metadata_transform.MetadataConvert().read_xml_info(xml_files[0],
                                                                       target_dir + '/' +
                                                                       entry.get() +
                                                                       '/dataset_description.json',
                                                                       entry.get())
            elif v.get() == 2:
                shutil.move(os.path.join('./', 'participants.tsv'),
                            os.path.join(target_dir, 'participants.tsv'))

            self.normal_buttons()
            self.delete_path()
        except ZeroDivisionError as err:
            messagebox.showerror("error", "list is empty")
            logging.error(err)
            self.normal_buttons()
        except FileNotFoundError as err:
            messagebox.showerror("error", "path not found")
            logging.error(err)
            self.normal_buttons()
        except NameError as err:
            messagebox.showerror("error", "target is not defined")
            logging.error(err)
            self.normal_buttons()
        except OSError as err:
            messagebox.showerror("error", "dataset name is not valid")
            logging.error(err)
            self.normal_buttons()

    def clicked_choose_input(self):
        """
        create new thread
        and start the choose method
        """
        threading.Thread(target=self.choose).start()

    def choose(self):
        """
        opens the file dialog and saves
        xml files
        """
        global ID_GUI
        global xml_files

        folder_selected = filedialog.askdirectory()
        self.clear_list()
        res = folder_selected
        try:
            xml_files = self.fast_scan(res)
            if v.get() == 1:
                data_dir_label.configure(text=os.path.basename(os.path.normpath(res)))
                if entry.get() == '':
                    entry.insert(0, os.path.basename(os.path.normpath(res)))
            elif v.get() == 2:
                exp_dir_label.configure(text=os.path.basename(os.path.normpath(res)))
        except FileNotFoundError as err:
            messagebox.showerror("error", "path not found")
            logging.error(err)
            self.normal_buttons()
        return 0

    @staticmethod
    def clicked_choose_target():
        """
        opens the file dialog and saves
        the specified path to directory
        """
        global ID_GUI
        global target_dir
        folder_selected = filedialog.askdirectory()

        res = folder_selected
        target_dir = res
        if v.get() == 1:
            data_tar_label.configure(text=os.path.basename(os.path.normpath(res)))
        elif v.get() == 2:
            exp_tar_label.configure(text=os.path.basename(os.path.normpath(res)))

    def fast_scan(self, dir_name):
        """
        finds vhdr and xml files in BrainVision project
        :param dir_name: directory path
        :return: list of xml files
        """
        dir_sub_sub = "name"
        global vhd_r_files
        vhd_r_files = []
        files = []
        sub_folders = [f.path for f in os.scandir(dir_name) if f.is_dir()]
        if len(sub_folders) > 0:
            dir_sub_sub = os.path.dirname(sub_folders[0])
            self.text.set(dir_sub_sub)
        for dir_sub in list(sub_folders):
            vhd_r_file = glob.glob(dir_sub + "/**/*.vhdr", recursive=True)
            xml_file = glob.glob(dir_sub + "/**/*.xml", recursive=True)

            if len(xml_file) > 0:
                files = files + xml_file

            if len(vhd_r_file) > 0:
                vhd_r_files = vhd_r_files + vhd_r_file
                for file_name in list(vhd_r_file):
                    if not re.match("^(.*target?).vhdr", file_name):
                        if v.get() == 1:
                            path = os.path.basename(os.path.normpath(dir_sub))
                        else:
                            path = os.path.basename(os.path.normpath(dir_sub_sub))
                        lb.insert("end", path)

        return files

    @staticmethod
    def clear_list():
        """
        deletes the entire list
        """
        lb.delete('0', 'end')
        vhd_r_files.clear()

    @staticmethod
    def delete_item():
        """
        deletes the entry from the list of vhdr files
        """
        selection = lb.curselection()
        if not selection or len(selection) < 1:
            return
        del vhd_r_files[selection[0]]
        lb.delete(selection[0])

    @staticmethod
    def disable_buttons():
        """
        disables buttons
        """
        entry.config(state="disable")
        exp_dir_button.config(state="disable")
        exp_tar_button.config(state="disable")
        data_dir_button.config(state="disable")
        data_tar_button.config(state="disable")
        transfer_button.config(state="disable")
        radiobutton_data.config(state="disable")
        radiobutton_experiment.config(state="disable")
        delete_button.config(state="disable")
        clear_button.config(state="disable")

    def delete_path(self):
        """
        set paths to default value
        """
        if v.get() == 1:
            self.clear_list()
            self.text.set("Directory dataset path")
        if v.get() == 2:
            self.clear_list()
            self.text.set("Directory experiment path")
        exp_dir_label.config(text="Original experiment location")

        exp_tar_label.config(text="Converted experiment location")

        data_dir_label.config(text="Original dataset location")

        data_tar_label.config(text="Converted dataset location")

    def normal_buttons(self):
        """
        set buttons to normal state
        """
        entry.config(state="normal")
        transfer_button.config(state="normal")
        radiobutton_data.config(state="normal")
        radiobutton_experiment.config(state="normal")
        delete_button.config(state="normal")
        clear_button.config(state="normal")
        self.show_choice()

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
        x_axis = win.winfo_screenwidth() // 2 - win_width // 2
        y_axis = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x_axis, y_axis))
        win.deiconify()


def main():
    """
    main method of the application
    """
    global root
    global v
    global logger
    logging.basicConfig(filename='errorBrainVisionToBids.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger(__name__)

    root = Tk()
    v = IntVar()
    v.set(1)
    global example
    example = GUI()
    Label(root)
    root.geometry("750x600+300+300")
    example.center(root)
    root.mainloop()


if __name__ == '__main__':
    main()
