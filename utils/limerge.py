#!/usr/bin/python

import argparse
from pathlib import Path
import os
import time
import glob


# --------------------------------------------------------------------------------------------------------------
def read_program_arguments():
    """ 
    reads the command line and validates the arguments. If everything goes well, it returns a list of strings
    with the pgn files for the next module to process
    
    param: command line arguments
    returns: a list of strings (file names/paths) for next processing
    """
    parser = argparse.ArgumentParser(
        description='This program generates a combined png file out of all the given pgn files.')
    parser.add_argument("-f", type=Path, required=True, help='Pass the folder containing png files')
    args = parser.parse_args()

    if not args.f.exists():
        print('The folder does not exist. Please provide a valid folder')
        exit(0)
    elif args.f.is_file():
        print('The path provided is a file. Please provide a folder containing png files to merge')
        exit(0)
    elif args.f.is_dir():
        files = contains_valid_files(args.f)
        return (files, args.f) if len(files) > 0 else ([], args.f)
    else:
        print('Invalid path found. Error!')
        exit(0)


# --------------------------------------------------------------------------------------------------------------
def contains_valid_files(folder):
    """
    Helper method to validate if the folder contains the pgn files for merging.
    
    param: the root folder which contains all the lichess files 
    returns: the actual pgn files strings contained in the root folder.
    """
    print('absolute path: ', folder.absolute())
    files = [f for f in glob.glob(os.fspath(folder.absolute()) + os.sep + '*.pgn')]
    return files


# --------------------------------------------------------------------------------------------------------------
def prepare_game_data(files):
    """
    Reads the list of files and collects the data in into a list

    param: list of files (paths) containing the chess games
    returns: a list of strings (each game data within the file)
    """
    print('Preparing game data...')
    all_game_data = [read_file(f) for f in files]
    return [] if len(all_game_data) == 0 else all_game_data


# --------------------------------------------------------------------------------------------------------------
def read_file(file):
    """
    Reads the pgn file and returns the content

    param: a pgn file to be read
    returns: the data within the pgn file
    """
    with open(file, "r") as f:
        return f.readlines()


# --------------------------------------------------------------------------------------------------------------
def write_to_disk(folder, game_data):
    """
    Writes the game data to the disk

    param: folder points to the path that was provided in the input. This is mainly used to
    param: all the game data (list of strings)
    returns: nothing. It writes the game data onto the disk in a single pgn file.
    """
    print('Writing to the disk')
    output_folder = os.fspath(folder.absolute()) + os.sep + 'merged'
    if not os.path.exists(output_folder):
        print ("creating the output folder: {}".format(output_folder))
        os.makedirs(output_folder)
    output_file = output_folder + os.sep + 'lichess_merged_' + time.strftime("%Y%m%d-%H%M%S") + '.pgn'
    with open(output_file, "w", encoding='utf-8') as f:
        for data in game_data:
            f.writelines(data)
    print('Done writing {} !'.format(output_file))


# ----------------------------------------MAIN METHOD------------------------------------------------------------
if __name__ == '__main__':
    all_files, path = read_program_arguments()
    all_data = prepare_game_data(all_files)
    write_to_disk(path, all_data)
