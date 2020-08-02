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
    messagebox, Entry, Scrollbar, Listbox, END, IntVar
from tkinter.ttk import Frame, Button, Label
from tkinter import filedialog
import brain_vision_converter
import metadata_transform
import progress_bar

ID_GUI = 1


class GUI(Frame):
    """
    GUI class
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        sets the appearance of the window
        """
        global data_dir_label
        global exp_dir_label
        global exp_tar_label
        global data_tar_label
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

        self.master.title("LukkoBids")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, pad=7)

        exp_dir_button = Button(self, text="Experiment directory", command=self.clicked_choose)
        exp_dir_button.grid(row=2, column=3)
        exp_dir_label = Label(self, text="Experiment name")
        exp_dir_label.grid(row=2, column=4, padx=5)

        exp_tar_button = Button(self, text="Experiment target", command=self.clicked_choose_target)
        exp_tar_button.grid(row=3, column=3, pady=4)
        exp_tar_label = Label(self, text="Directory name")
        exp_tar_label.grid(row=3, column=4, padx=5)

        data_dir_button = Button(self, text="Dataset directory", command=self.clicked_choose)
        data_dir_button.grid(row=2, column=0)
        data_dir_label = Label(self, text="Dataset name")
        data_dir_label.grid(row=2, column=1, padx=5)

        data_tar_button = Button(self, text="Dataset target", command=self.clicked_choose_target)
        data_tar_button.grid(row=3, column=0, pady=4)
        data_tar_label = Label(self, text="Directory name")
        data_tar_label.grid(row=3, column=1)

        data_name_label = Label(self, text="Dataset name: ")
        data_name_label.grid(row=1, column=0, padx=5)

        entry = Entry(self)
        entry.grid(row=1, column=1, pady=6)

        transfer_button = Button(self, text="Transfer data", command=self.clicked_transfer)
        transfer_button.grid(row=4, column=2, padx=5)

        scrollbar = Scrollbar(self, orient="vertical")
        lb = Listbox(self, yscrollcommand=scrollbar.set)
        scrollbar.config(command=lb.yview)

        lb.grid(row=5, column=0, columnspan=5, rowspan=1,
                padx=5, sticky=E+W+S+N)

        radiobutton_data = Radiobutton(self,
                                       text="ADD dataset",
                                       padx=20,
                                       variable=v,
                                       command=self.show_choice,
                                       value=1)
        radiobutton_experiment = Radiobutton(self,
                                             text="ADD experiment",
                                             padx=20,
                                             variable=v,
                                             command=self.show_choice,
                                             value=2)
        radiobutton_data.grid(row=0, column=0)
        radiobutton_experiment.grid(row=0, column=3)

        delete_button = Button(self, text="Delete", command=self.delete_item)
        clear_button = Button(self, text="Clear", command=self.clear_list)
        delete_button.grid(row=6, column=0)
        clear_button.grid(row=6, column=4)

        self.show_choice()

    @staticmethod
    def show_choice():
        """
        sets the visibility of the buttons
         according to the radio buttons
        """
        if v.get() == 1:
            exp_dir_button.config(state="disable")
            exp_tar_button.config(state="disable")
            data_dir_button.config(state="normal")
            data_tar_button.config(state="normal")
        if v.get() == 2:
            exp_dir_button.config(state="normal")
            exp_tar_button.config(state="normal")
            data_dir_button.config(state="disable")
            data_tar_button.config(state="disable")
        print(v.get())

    @staticmethod
    def next_id():
        """
        counter id
        """
        global ID_GUI
        ID_GUI += 1
        res = ID_GUI
        return res

    def clicked_transfer(self):
        """
        disable buttons and then start new thread
        which start transform data
        """
        self.disable_buttons()
        threading.Thread(target=self.transform_data).start()

    def transform_data(self):

        if v.get() == 1:
            metadata_transform.MetadataConvert().create_meta_data_file()
        if v.get() == 2:
            shutil.move(os.path.join(target_dir, 'participants.tsv'), os.path.join('./', 'participants.tsv'))

        progress_bar.ProgressBar().start()
        progress_step = float(100.0 / lb.size())
        for i, listbox_entry in enumerate(lb.get(0, END)):
            progress_bar.ProgressBar().update_progress(progress_step)
            print(listbox_entry)
            if v.get() == 1:
                brain_vision_converter.BrainVisionConverter()\
                    .transform_data_to_bids_call(listbox_entry,
                                                 entry.get(), target_dir)
            elif v.get() == 2:
                brain_vision_converter.BrainVisionConverter().\
                    get_id(target_dir)
                brain_vision_converter.BrainVisionConverter().\
                    transform_data_to_bids_call_experiment(listbox_entry,
                                                           target_dir)

        progress_bar.ProgressBar().exit_progress()
        if v.get() == 1:
            shutil.move(os.path.join('./', 'participants.tsv'),
                        os.path.join(target_dir + '/' + entry.get(),
                                     'participants.tsv'))

            metadata_transform.MetadataConvert().read_xml_info(xml_files[0],
                                                               target_dir + '/' +
                                                               entry.get() +
                                                               '/dataset_description.json',
                                                               entry.get())
        elif v.get() == 2:
            shutil.move(os.path.join('./', 'participants.tsv'),
                        os.path.join(target_dir, 'participants.tsv'))

        self.normal_buttons()

    def clicked_choose(self):
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

        res = folder_selected
        try:
            xml_files = self.fast_scan(res)
            if v.get() == 1:
                data_dir_label.configure(text=os.path.basename(os.path.normpath(res)))
            elif v.get() == 2:
                exp_dir_label.configure(text=os.path.basename(os.path.normpath(res)))
        except FileNotFoundError:
            messagebox.showerror("error", "path not found")
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

    @staticmethod
    def fast_scan(dir_name):
        """
        finds vhdr and xml files in BrainVision project
        :param dir_name: directory path
        :return: list of xml files
        """
        files = []
        sub_folders = [f.path for f in os.scandir(dir_name) if f.is_dir()]
        print(sub_folders)
        for dir_sub in list(sub_folders):
            vhd_r_files = glob.glob(dir_sub + "/**/*.vhdr", recursive=True)
            xml_file = glob.glob(dir_sub + "/**/*.xml", recursive=True)

            if len(xml_file) > 0:
                files = files + xml_file

            if len(vhd_r_files) > 0:
                for file_name in list(vhd_r_files):
                    lb.insert("end", file_name)

        print(files)
        return files

    @staticmethod
    def clear_list():
        """
        deletes the entire list
        """
        lb.delete('0', 'end')

    @staticmethod
    def delete_item():
        """
        deletes the entry from the list of vhdr files
        """
        selection = lb.curselection()
        if not selection or len(selection) < 1:
            return
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
