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
directory = r"C:\KP Python\Movie deduper\test"

os.chdir(directory) # change cwd to the desired directory
abspath = os.path.abspath('.')  # define abspath


def get_video_filename_and_size(fname, folname):
    movie_extensions = ['.mov', '.mp4', '.mkv']
    basename, ext = os.path.splitext(fname) # isolate basename and extensions
    if ext in movie_extensions:
        # print('Movie file detected in {}: {}'.format(folname, fname))
        fname_with_path = os.path.join(abspath, folname, fname)    # new name incl path
        return fname, os.path.getsize(fname_with_path)

for folderName, subfolders, filenames in os.walk(directory):
    # print('The current folder is ' + folderName)
    # for subfolder in subfolders:
    #    print('SUBFOLDER OF ' + folderName + ': ' + subfolder)
    movie_files_detected = []
    for filename in filenames:
    #   print('FILE INSIDE ' + folderName + ': ' + filename)
        if get_video_filename_and_size(filename, folderName) != None:
            movie_files_detected.append(get_video_filename_and_size(filename, folderName))
        # print('Base name is {} and extension is {}'.format(basename, ext))
    if len(movie_files_detected) > 0:
        print('Movie files detected in {} = {}'.format(folderName, movie_files_detected))
    # TO DO: determine largest video file
    for name_size_pair in movie_files_detected:
        name = name_size_pair[0]
        size = name_size_pair[1]
        print('Name = {} and size = {}'.format(name, size))
        # hmmm... how do I now compare the size in each tuple to find the largest? there is a list command but
        #  these aren't in a list. Could try using a for loop to cycle through each and compare?


#  for filename in os.listdir(os.getcwd()):

# code to list base names and extensions






