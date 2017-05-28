#! python3
# Deduper.py - Script to crawl through Movies directory, notify if multiple video files and prompt to delete all but
# the largest of the files found in each directory. Perhaps even delete all files (non video files included)

# TO DO:
# crawl through each file in each directory
# print the name of each folder and its containing files including extension
# print only those folder and file names which have a mov m4v mp4 mkv extension
# print only the folder name, and video file names, of directories containing multiple video files
# isolate the largest and non-largest video files
# prompt asking if user wants to delete non-largest video files

import os

# directory = str(sys.argv[1])  # takes the desired directory from the command line argument, passed by the batch file
directory = r"C:\KP Python\deduper\test"

os.chdir(directory) # change cwd to the desired directory
abspath = os.path.abspath('.')  # define abspath


def get_video_filename(fname, folname):
    movie_extensions = ['.mov', '.mp4', '.mkv']
    basename, ext = os.path.splitext(fname) # isolate basename and extensions
    if ext in movie_extensions:
        # print('Movie file detected in {}: {}'.format(folname, fname))
        fname_with_path = os.path.join(abspath, folname, fname)    # new name incl path
        return fname_with_path

for folderName, subfolders, filenames in os.walk(directory):
    # print('The current folder is ' + folderName)
    # for subfolder in subfolders:
    #    print('SUBFOLDER OF ' + folderName + ': ' + subfolder)
    movie_files_detected = []
    for filename in filenames:
    #   print('FILE INSIDE ' + folderName + ': ' + filename)
        if get_video_filename(filename, folderName) != None:
            movie_files_detected.append(get_video_filename(filename, folderName))
    # TO DO: sort and print video files
    fname_sorted = sorted(movie_files_detected, key=os.path.getsize, reverse=True)
    for item in fname_sorted:
        print('item is {}, size is {}'.format(item, os.path.getsize(item)))
    # TO DO: print video files which can be deleted
    if len(fname_sorted) >= 1:
        print('Multiple video files detected.')
        print('Potential files to delete are as follows:')
        for i in range(1, len(fname_sorted)):
            print('File to delete is {}, size is {}'.format(fname_sorted[i], os.path.getsize(fname_sorted[i])))
        for i in range(1, len(fname_sorted)):
            response = input('Press Y to delete or N to ignore: {}, size is {}'.format(fname_sorted[i], os.path.getsize(fname_sorted[i])))
            response.upper()
            if response == 'Y':
                print('Pretending to delte file: {}'.format(fname_sorted[i])) # INSERT CODE TO DELETE FILE
            else:
                continue
