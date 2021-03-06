#! python3
# Deduper.py - Script to crawl through Movies directory, notify if multiple video files and prompt to delete all but
# the largest of the files found in each directory. Ultimately can have CLI and GUI options.

# TO DO:
# establish how to run from CLI or GUI
# Fix output capacity issue on text box
# refactor where sensible - e.g. move output statement for first file into class
# make it pretty


import os
import send2trash
from tkinter import *

Test_mode = True


def tell_me_which_directory():
    if len(sys.argv) > 1:
        direc = str(sys.argv[1])  # takes the desired directory from the command line argument, passed by the batch file
    else:
        if os.path.exists(r"C:\Program Files\StableBit\DrivePool"):
            print("Kev's Home PC detected, setting default test directory accordingly\n")
            direc = r"C:\Github local repos\deduper\test"   # note this this the hardcoded directory for when working on Home PC
        else:
            print("This isn't Kev's Home PC, must be laptop, so setting test default directory accordingly\n")
            direc = r"C:\KP Python\deduper\test"
    try:
        if gui.dir_set_by_button:
            direc = gui.get_dir_from_gui()
    except:
        print('KP Error - gui.dir_set_by_button is not found')
    return direc


def get_video_filename(fname, folname, abspath):
    movie_extensions = ['.mov', '.mp4', '.mkv', '.avi']
    basename, ext = os.path.splitext(fname) # isolate basename and extensions
    if ext in movie_extensions:
        # print('Movie file detected in {}: {}'.format(folname, fname))
        fname_with_path = os.path.join(abspath, folname, fname)    # new name incl path
        return fname_with_path


def main_fn():
    directory = tell_me_which_directory()
    print('Directory = {}'.format(directory))
    os.chdir(directory) # change cwd to the desired directory
    abspath = os.path.abspath('.')  # define abspath
    for folderName, subfolders, filenames in os.walk(directory):
        movie_files_detected = []
        for filename in filenames:
            if get_video_filename(filename, folderName, abspath) != None:
                movie_files_detected.append(get_video_filename(filename, folderName, abspath))
        fname_sorted = sorted(movie_files_detected, key=os.path.getsize, reverse=True)
        if len(fname_sorted) > 1:
            print('Multiple video files detected in folder {}'.format(folderName))
            print("The largest video file in the folder, which we won't touch, is {}\n".format(fname_sorted[0]))
            print('Potential files to delete are as follows:')
            for i in range(1, len(fname_sorted)):
                print('File to delete is {}, size is {}'.format(fname_sorted[i], os.path.getsize(fname_sorted[i])))
            for i in range(1, len(fname_sorted)):
                response = input('\nPress Y to delete or N to ignore: {}, size is {}\n'.format(fname_sorted[i],
                                                                                               os.path.getsize(
                                                                                                   fname_sorted[i])))
                response = response.upper()
                if response == 'Y':
                    if not Test_mode:
                        print('Sending to Recycle Bin: {}'.format(fname_sorted[i]))
                        send2trash.send2trash(fname_sorted[i])
                    else:
                        print('Pretending to delete file: {}'.format(fname_sorted[i]))  # INSERT CODE TO DELETE FILE
                else:
                    continue
    while True:
        q = input('Press Q to quit\n')
        q = q.upper()
        if q == 'Q':
            sys.exit()


def main_alt():     # this is the new 'Main' function for when using GUI

    direc = tell_me_which_directory()
    gui.output('Directory = {}\n\n'.format(direc))
    os.chdir(direc) # change cwd to the desired directory
    abspath = os.path.abspath('.')  # define abspath
    for folderName, subfolders, filenames in os.walk(direc):
        movie_files_detected = []
        for filename in filenames:
            if get_video_filename(filename, folderName, abspath) != None:
                movie_files_detected.append(get_video_filename(filename, folderName, abspath))
        fname_sorted = sorted(movie_files_detected, key=os.path.getsize, reverse=True)
        if len(fname_sorted) > 1:
            gui.output('\n\n\nMultiple video files detected in folder {}'.format(folderName))   #temp commented out as text box full
            gui.output("The largest video file in the folder, which we won't touch, is {}\n".format(fname_sorted[0]))
            # gui.output('Potential files to delete are as follows:')

            for i in range(1, len(fname_sorted)):
                # gui.output('File to delete is {}, size is {}'.format(fname_sorted[i], os.path.getsize(fname_sorted[i])))
                gui.to_delete.append(fname_sorted[i])   # add non-largest videos to the 'To Delete' list
    # gui.output(gui.to_delete)
    # gui.output("Press 'DEL' to delete File #{} - {}".format(gui.index+1, gui.to_delete[gui.index]))   # Displays first file only
    gui.show_next_file()

class Gui:
    def __init__(self, root):

        self.index = -1
        self.to_delete = []

        self.text_box = Text(root, height=30, width=120)
        self.text_box.grid(row=5, column=2)

        self.labelHeading = Label(root, text='Deduper', font = 'Arial 24 bold', fg='blue', bg='gray')
        self.labelHeading.grid(row=0, column=2)
        self.labelDescription = Label(root, text='Deletes all but the largest video file in each sub-dir', font='Arial 16', fg='blue', bg='gray')
        self.labelDescription.grid(row=1, column=2)

        self.labelDir = Label(root, text='Directory', font='Arial 16', fg='blue', bg='gray')
        self.labelDir.grid(row=2, column=1)
        self.entryDir = Entry(root, width=50)
        self.entryDir.insert(10, dir_text)
        self.entryDir.grid(row=2,column=2)

        self.quitButton = Button(root,text='Quit', font='Arial 16',command=quit, fg='red', bg='gray')
        self.quitButton.grid(row=4,column=1)

        self.goButton = Button(root,text='Go', font='Arial 24 bold',command=self.main_triggered_from_button, fg='green', bg='gray')
        self.goButton.grid(row=4,column=3)

        self.dontdeleteButton = Button(root, text='Dont delete', font='Arial 16', command=self.dont_delete, fg='yellow', bg='gray', state='disabled')
        self.dontdeleteButton.grid(row=3, column=2)

        self.deleteButton = Button(root, text='DELETE', font='Arial 16', command=self.delete_file, fg='red', bg='gray', state='disabled')
        self.deleteButton.grid(row=4, column=2)

        self.abortButton = Button(root, text='Abort', font='Arial 16', command=self.end_program, fg='red', bg='gray', state='disabled')
        self.abortButton.grid(row=3, column=3)

        self.dir_set_by_button = False

    def dont_delete(self):    # don't delete, just move to the next file
        gui.output("Ignoring File #{} - {}".format(self.index+1, self.to_delete[self.index]))
        self.show_next_file()

    def delete_file(self):
        if not Test_mode:
            gui.output("Sending to Recycle Bin #{} - {}".format(self.index+1, self.to_delete[self.index]))
            send2trash.send2trash(self.to_delete[self.index])
        else:
            gui.output("Test mode - pretending to delete #{} - {}".format(self.index+1, self.to_delete[self.index]))
        self.show_next_file()

    def show_next_file(self):
        self.check_if_all_files_processed()
        self.index += 1
        try:
            gui.output("\nDo you want to delete File #{} - {}?".format(self.index+1, self.to_delete[self.index]))
        except IndexError:
            print('Show_next_file() Index Error: Index out of range (program should now be complete)')

    def enable_dir_set_by_button(self):
        self.dir_set_by_button = True

    def main_triggered_from_button(self):
        self.enable_dir_set_by_button()
        self.disable_go_button()
        self.enable_all_buttons()
        main_alt()

    def get_dir_from_gui(self):
        self.new_dir = gui.entryDir.get()
        print('Attempting to set new dir')
        return self.new_dir

    def output(self, text):
        self.text_box.insert(END, '{}\n'.format(text))
        self.text_box.see(END)    # not sure if this updates the text, or tells the text box to scroll if needed
        print('Attempting to OUTPUT: {}\n'.format(text))
        print(text)

    def check_if_all_files_processed(self):
        if self.index >= len(self.to_delete)-1:
            self.end_program()

    def end_program(self):
        self.output("Program ended. Quit or change directory and go again")
        self.disable_all_buttons()
        self.reset_stats()
        self.enable_go_button()

    def disable_go_button(self):
        self.goButton.config(state='disabled')

    def enable_go_button(self):
        self.goButton.config(state='normal')

    def disable_all_buttons(self):
        self.dontdeleteButton.config(state='disabled')
        self.deleteButton.config(state='disabled')
        self.abortButton.config(state='disabled')

    def enable_all_buttons(self):
        self.dontdeleteButton.config(state='normal')
        self.deleteButton.config(state='normal')
        self.abortButton.config(state='normal')

    def reset_stats(self):
        self.index = 0
        self.to_delete = []


directory = tell_me_which_directory()   # determine directory
dir_text = str(directory)   # converts directory path to text for use by tkinter 'entryDir' as default text

root = Tk().title('Deduper')    # establish Gui object with tkinter
gui = Gui(root)                 # establish Gui object with tkinter
gui.output('Hello, this script will crawl through the directory and sub-dirs, notify if multiple video files found in'
           ' one dir, and prompt to delete each of them, excluding the largest one\n\n\n')
mainloop()                      # fundamental tkinter loop
