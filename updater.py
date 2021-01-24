# Simple updater script that returns the flag of status from a git pull

import git

def updater():
    repo = git.Repo("~/git/RobotMark")
    status = repo.remotes.origin.pull()

    return status[0].flags






