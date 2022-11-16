# List dirs in a masterdir
# Determine for each dir if there is a .git
# Determine for .git if the branch is up-to-date or if there are untracked

import os, sys

def findGitRepos(dirpath):
    gitRepos = []
    for dir in os.listdir(dirpath):
        dpath = os.path.join(dirpath, dir)
        if os.path.isdir(dpath):
            if '.git' in os.listdir(dpath):
                gitRepos.append(dpath)
    return gitRepos

def checkRepo(repopath):
    loc = os.getcwd()
    os.system('cd {}'.format(repopath))
    os.system('git diff --name-only > temp_git_analysis.txt')
    f = open('temp_git_analysis.txt','r')
    num_diffs = len(f.readlines())
    print(f.readlines())
    f.close()
    os.system('rm temp_git_analysis.txt')
    os.system('cd {}'.format(loc))
    return num_diffs

def manageRepos(dirpath):
    print('')
    print('Found Git Repos under {}:'.format(dirpath))
    print('')
    repos = findGitRepos(dirpath)
    for repo in repos:
        print(repo.split('/')[-1],end=': ')
        print(checkRepo(repo))


mydir = '/home/dwest77/Documents/'

manageRepos(mydir)