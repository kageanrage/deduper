#! python3
# Deduper.py - Script to crawl through Movies directory, notify if multiple video files and prompt to delete all but
# the largest of the files found in each directory


import os
import send2trash
import sys


Test_mode = True

def set_directory():
    if len(sys.argv) > 1:
        dir = str(sys.argv[1])  # takes the desired directory from the command line argument, passed by the batch file
    else:
        if os.path.exists(r"C:\Program Files\StableBit\DrivePool"):
            print("Kev's Home PC detected, setting default test directory accordingly\n")
            dir = r"C:\Github local repos\deduper\test"   # note this this the hardcoded directory for when working on Home PC
        else:
            print("This isn't Kev's Home PC, must be laptop, so setting test default directory accordingly\n")
            dir = r"C:\KP Python\deduper\test"
    return dir


def get_video_filename(fname, folname):
    movie_extensions = ['.mov', '.mp4', '.mkv', '.avi']
    basename, ext = os.path.splitext(fname) # isolate basename and extensions
    if ext in movie_extensions:
        # print('Movie file detected in {}: {}'.format(folname, fname))
        fname_with_path = os.path.join(abspath, folname, fname)    # new name incl path
        return fname_with_path


directory = set_directory()
os.chdir(directory) # change cwd to the desired directory
abspath = os.path.abspath('.')  # define abspath


print('Hello, this script will crawl through the directory and sub-dirs, notify if multiple video files found in one '
      'dir, and prompt to delete each of them, excluding the largest one\n\n\n')
for folderName, subfolders, filenames in os.walk(directory):
    movie_files_detected = []
    for filename in filenames:
        if get_video_filename(filename, folderName) != None:
            movie_files_detected.append(get_video_filename(filename, folderName))
    fname_sorted = sorted(movie_files_detected, key=os.path.getsize, reverse=True)
    if len(fname_sorted) >= 1:
        print('Multiple video files detected in folder {}'.format(folderName))
        print("The largest video file in the folder, which we won't touch, is {}\n".format(fname_sorted[0]))
        print('Potential files to delete are as follows:')
        for i in range(1, len(fname_sorted)):
            print('File to delete is {}, size is {}'.format(fname_sorted[i], os.path.getsize(fname_sorted[i])))
        for i in range(1, len(fname_sorted)):
            response = input('\nPress Y to delete or N to ignore: {}, size is {}\n'.format(fname_sorted[i], os.path.getsize(fname_sorted[i])))
            response = response.upper()
            if response == 'Y':
                if not Test_mode:
                    print('Sending to Recycle Bin: {}'.format(fname_sorted[i]))
                    send2trash.send2trash(fname_sorted[i])
                else:
                    print('Pretending to delete file: {}'.format(fname_sorted[i])) # INSERT CODE TO DELETE FILE
            else:
                continue
