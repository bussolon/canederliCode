#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pan2epdf.py

Created by [Stefano Bussolon ](<http://www.bussolon.it>)
with the help of gemini-1.5-flash-002
14/11/2024

The script `git_file_history.py` takes the path to a file as a command-line argument and displays the history of changes made to that file within a Git repository.  
It searches upward from the file's location to find the nearest Git repository. 
For each commit affecting the specified file, it retrieves the commit date and message,  presenting them in a chronologically reverse-ordered, concatenated string.  
Error handling is included to manage situations where the file path is invalid, the repository is not found or there are issues with Git commands.


"""

import sys
import os
import git
import datetime

def get_file_changes(file_path):
    """
    Lists all changes to a specific file in a Git repository.

    Args:
        file_path: Path to the file within the repository.

    Returns:
        
    """
    repo_path = None
    abs_path = os.path.abspath(file_path)  #Ensure absolute path for better traversal
    print (f"abs_path:  {abs_path}")
    current_dir = os.path.dirname(abs_path)

    while current_dir != '/' and current_dir != os.path.sep: #Traverse upwards until root or repo found
        if os.path.exists(os.path.join(current_dir, ".git")):
            repo_path = current_dir
            print (f"repo_path: {repo_path}")
            break
        current_dir = os.path.dirname(current_dir)

    if repo_path is None:
        print("Error: Could not find a Git repository containing the specified file.")
        return None
    try:
        repo = git.Repo(repo_path)
        commits = list(repo.iter_commits('--all', paths=file_path))  #Efficiently get only commits affecting the file
        lista = ""
        for commit in commits[::-1]:
            #print(dir(commit))
            dataInt = commit.committed_date
            datString = datetime.datetime.fromtimestamp(dataInt).strftime('%Y-%m-%d %H:%M:%S')
            messaggio = commit.message
            formattato = f"{datString}: {messaggio}"
            lista += formattato
            #print(formattato)
            # ~ diff = commit.diff(commit.parents[0] if commit.parents else None, paths=[file_path]) #handle initial commit
        print (lista)
        return lista

        # ~ return changes

    except git.exc.InvalidGitRepositoryError:
        print(f"Error: '{repo_path}' is not a valid Git repository.")
        return None
    except git.exc.GitCommandError as e:
        print(f"Git command error: {e}")
        return None
    except IndexError: #Handle commits without parent (initial commit)
        print("Error: Commit has no parent.")
        return None
    except Exception as e: #Catch other potential exceptions
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    # Check if the user provided an argument
    if len(sys.argv) != 2:
        print("Please provide the path of the file.")
        sys.exit(1)

    # Get the argument from the command line
    nomeFile = sys.argv[1]
    # Call get_file_changes with the argument
    get_file_changes(nomeFile)

