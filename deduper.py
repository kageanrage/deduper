#! python3
# Deduper.py - Script to crawl through Movies directory, notify if multiple video files and prompt to delete all but
# the largest of the files found in each directory

# TO DO:
# show all text on GUI instead of in command prompt / console


import os
import send2trash
import sys
from tkinter import *

Test_mode = True

dir_set_by_button = False


def enable_dir_set_by_button():
    global dir_set_by_button
    dir_set_by_button = True


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
    if dir_set_by_button:
        direc = get_dir_from_gui()
    return direc


def get_dir_from_gui():
    new_dir = entryDir.get()
    print('Attempting to set new dir')
    return new_dir


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


def main_triggered_from_button():
    enable_dir_set_by_button()
    main_fn()

print('Hello, this script will crawl through the directory and sub-dirs, notify if multiple video files found in one '
      'dir, and prompt to delete each of them, excluding the largest one\n\n\n')

directory = tell_me_which_directory()
dir_text = str(directory)   # converts directory path to text for use by tkinter 'entryDir' as default text

# TKINTER SECTION
root = Tk()
root.title('Deduper')

labelHeading = Label(root, text='Deduper', font = 'Arial 24 bold', fg='blue', bg='gray').grid(row=0, column=2)
labelDescription = Label(root, text='Deletes all but the largest video file in each sub-dir', font='Arial 16', fg='blue', bg='gray').grid(row=1, column=2)

labelDir = Label(root, text='Directory', font='Arial 16', fg='blue', bg='gray').grid(row=2, column=1)
entryDir = Entry(root, width=50)
entryDir.insert(10, dir_text)
entryDir.grid(row=2,column=2)


quitButton = Button(root,text='Quit', font='Arial 16',command=quit, fg='red', bg='gray').grid(row=4,column=1)
goButton = Button(root,text='Go', font='Arial 24 bold',command=main_triggered_from_button, fg='green', bg='gray').grid(row=4,column=3)
mainloop()


# PRESS Q TO QUIT


