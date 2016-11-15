#!/usr/bin/env python

#Script to check whether the output files generated by HCP pipeline scripts are the same or not. It will check for the match between two files with respect the filename, size, content, modification time, distance etc.
#Maintainters : Big Data Lab Team, Concordia University.
#email : tristan.glatard@concordia.ca, laletscaria@yahoo.co.in

import os
import sys
import subprocess
import argparse
import hashlib
from collections import defaultdict,OrderedDict
#study_folder_dict is an orderd python dictionary for storing the details regarding the files of  individual subjects. Key : Relative file name, Value : Corresponding file_dir_dict
study_folder_dict = OrderedDict()
#Method list_files_and_dirs is used for listing files and directories present in the input directory.
#Input Argument : Directory Path
def list_files_and_dirs(dirPath):
        listFileAndDirs = []
	rootDir = dirPath
        for dir_, _, files in os.walk(rootDir):
           listFileAndDirs.append(os.path.relpath(dir_, rootDir))
           for fileName in files:
              relDir = os.path.relpath(dir_, rootDir)
              relFile = os.path.join(relDir, fileName)
              listFileAndDirs.append(relFile)
	#Sort the files and subdirectories according to the modification time.
        listFileAndDirs.sort(key=lambda x: os.path.getmtime(os.path.join(rootDir,x)))
	return listFileAndDirs

#Method populate_file_dir_dict is an ordered  python dictionary to save the status details of
#each file and directory present in the listFileAndDirs list
#Input parameter : List contianing the details of the path of each file and directory.
def populate_file_dir_dict(listFileAndDirs,dirPath):
        temp_dict = OrderedDict(defaultdict(list))
        for relPath in listFileAndDirs:
	   sha256_digest = generate_checksum(dirPath,relPath)
           dirDetails=os.stat(os.path.join(dirPath,relPath))
	   temp_dict.setdefault(relPath, []).append(sha256_digest)
	   temp_dict.setdefault(relPath, []).append(dirDetails)
	   #temp_dict[relPath]=sha256_digest
           #temp_dict[relPath].append(dirDetails)
        return temp_dict

#Method populate_study_folder_dict will store the details regarding each subject folder in an ordered python dictionary. Key : Folder or file name , Value : dictionary with details of the key value
def populate_study_folder_dict(file_path):
	temp_study_folder_dict=OrderedDict()
	#study_folders_list : List contians all the subject folder paths
	study_folders_list=read_contents_from_file(file_path)
	for folder in study_folders_list:
	   #fileNamesAndDirArray is used to store the relative path of the directories and files present in the directory given as input.
           fileNamesAndDirArray=[]
           #file_dir_dict is an ordered  python dictionary used to store the details of individual files.Key : Relative file path, Value : Status info
           file_dir_dict=OrderedDict()
	   fileNamesAndDirArray=list_files_and_dirs(folder)
	   file_dir_dict=populate_file_dir_dict(fileNamesAndDirArray,folder)
	   temp_study_folder_dict[folder]=file_dir_dict
	return temp_study_folder_dict

#read_contents_from_file method is used to read the directory path containing the subject folders.
def read_contents_from_file(fileDir): 
# Open the file for reading.
	with open(fileDir, 'r') as infile:
	   data = infile.read()  # Read the contents of the file into memory.
	   #Return a list of the lines, breaking at line boundaries.
	   directory_list = data.splitlines()
	   return directory_list

def generate_checksum(rootdir, filename):
    blocksize=2**20
    hasher = hashlib.sha256()
    if os.path.isfile(os.path.join(rootdir, filename)):
       with open( os.path.join(rootdir, filename) , "rb" ) as f:
           while True:
               buf = f.read(blocksize)
               if not buf:
                   break
               hasher.update( buf )
       return hasher.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_in', help='Input the text file containing the path to the subject folders')
    args = parser.parse_args()
    total = len(sys.argv)
    cmdargs = str(sys.argv)
    print ("The total numbers of args passed to the script: %d " % total)
    print ("Args list: %s " % cmdargs)
    print ("Script name: %s" % str(sys.argv[0]))
    print ("First argument: %s" % str(sys.argv[1]))
    study_folder_dict=populate_study_folder_dict(sys.argv[1])
    print study_folder_dict

if __name__ == '__main__':
    main()
