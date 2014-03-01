#! /usr/bin/env python
__author__ = 'Martin Leinberger'

import os
import sys
import json
import urllib2

from git import Repo, ChangeObject
import log
import lib

sys.path.append('../../libraries/101meta')
import const101

# Global variables
root_repo_url = const101.url101repo.replace('/tree/master/', '')
deps_url = 'http://101companies.org/pullRepo.json'



def main():
    # Check out the "root" repo (101companies/101repo)
    root = Repo(url=root_repo_url, path=const101.sRoot)
    changes = root.cloneOrPull()

    # Next, handle the dependencies by transforming them into something that is easier to handle
    instructions = lib.transformToInstructions(json.load(urllib2.urlopen(deps_url)))

    # We need to track whether members got removed from the instruction set or complete repos are no longer needed
    # To enable this, we need to know which members are already mounted and which repos are already cloned
    mounted_members = lib.collectMountedMembers()
    cloned_repos = lib.collectClonedRepos()

    # After that, update the soft links
    for instruction in instructions:
        # For all instructions, update (clone/pull) the repo which will yield a list of changed files and the info
        # whether a repo is cloned. If it is not cloned, then we remove it from our book-keeping, as this repo is
        # handled. Also, we add the changes to the list of changes
        changes_in_repo = instruction.updateRepo()
        if instruction.checkoutTo in cloned_repos:
            cloned_repos.remove(instruction.checkoutTo)
        changes += changes_in_repo

        # Now we update member mounts. If the mount is already known, we can remove it from book-keeping. If it is not
        # in the list, it was newly created (and we don't need to do anything).
        for sl_instruction in instruction.softLinkInstructions:
            sl_instruction.updateLink()
            if sl_instruction.mountAt in mounted_members:
                mounted_members.remove(sl_instruction.mountAt)

    # Finally we can take a look at the stuff that is still in our book-keeping lists. Those must be deprecated as
    # there were no instruction dealing with them. Therefore we can remove these
    for member in mounted_members:
        for root, dirs, files in os.walk(member, followlinks=True):
            if not '.git' in root:
                for file in files:
                    changes.append( ChangeObject('DEL', file) )
        os.remove(member)
    for repo in cloned_repos:
        if os.path.exists(repo):
            os.removedirs(repo)


    # At last, save changes to a log file
    log.Changes.add(changes)
    log.Changes.save()

if __name__ == '__main__':
    main()

