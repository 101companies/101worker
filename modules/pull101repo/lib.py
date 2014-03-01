__author__ = 'Martin Leinberger'

import sys
import re
import os
import commands

import git
import const101


# Logging definitions
__LOG_MASK = 0xf

_REPO_ACTION = 0x1
_LINK_ACTION = 0x0
_CHANGE_REWRITE_ACTION = 0x4


def log(msg, action):
    if action & __LOG_MASK:
        print msg
        sys.stdout.flush()


def collectMountedMembers():
    mounted_members = []
    if os.path.exists(const101.sRoot):
        for namespace in os.listdir(const101.sRoot):
            if os.path.isdir(os.path.join(const101.sRoot, namespace)):
                for member in os.listdir(os.path.join(const101.sRoot, namespace)):
                    path = os.path.join(const101.sRoot, namespace, member)
                    if os.path.islink(path):
                        mounted_members.append(path)
    return mounted_members


def collectClonedRepos():
    cloned_repos = []
    base_path = os.path.join(const101.results101, 'gitdeps')
    if os.path.exists(base_path):
        for username in os.listdir(base_path):
            for repo in os.listdir(os.path.join(base_path, username)):
                if os.path.exists(os.path.join(base_path, username, repo, '.git')):
                    cloned_repos.append(os.path.join(base_path, username, repo))
    return cloned_repos


def splitRepoUrl(url):
    """
    @type url: str
    """
    pattern = 'https://github.com/([^/]+)/([^/]+)(/tree/master/?(.*))?'
    user_name, repo_name, _, sub_path = re.search(pattern, url).groups()
    if not sub_path:
        sub_path = ''
    return user_name, repo_name, sub_path


def transformToInstructions(dependencies):
    """

    @rtype : list of RepoInstruction
    @type dependencies: dict
    """
    instructions = {}

    # Iterate over all entries in the dependencies and convert to instruction if they are not contained in the base
    # version of 101repo
    for namespace in dependencies.keys():
        for member in dependencies[namespace].keys():
            if not const101.url101repo in dependencies[namespace][member]:
                # Split the info from the dependencies into the basic parts
                user_name, repo_name, path_in_repo = splitRepoUrl(dependencies[namespace][member])
                # Now, create all necessary URLs and paths from it
                repo_url = 'https://github.com/{}/{}'.format(user_name, repo_name)
                checkout_to = os.path.join(const101.results101, 'gitdeps', user_name, repo_name)
                mount_at = os.path.join(const101.sRoot, namespace, member)
                point_to = os.path.join(checkout_to, path_in_repo)

                if not repo_url in instructions:
                    instructions[repo_url] = RepoInstruction(repo_url=repo_url, checkout_to=checkout_to)
                instructions[repo_url].addLinkInstruction(SoftLinkInstruction(mount_at=mount_at, point_to=point_to))

    return instructions.values()


class SoftLinkInstruction:
    def __init__(self, mount_at, point_to):
        """
        @type mount_at: str
        @type point_to: str
        """
        self.__mount_at = mount_at
        self.__point_to = point_to

    @property
    def mountAt(self):
        return self.__mount_at

    @property
    def pointTo(self):
        return self.__point_to

    def __str__(self):
        return '({} -> {})'.format(self.mountAt, self.pointTo)

    def __repr__(self):
        return self.__str__()

    def updateLink(self):
        # If link exists, but points somewhere different, we must remove it (will be recreated at end of this method)
        if os.path.islink(self.mountAt) and not os.readlink(self.mountAt) == self.pointTo:
            log("Removing {}, because it points to {}, but should instead point to {}".format(self.mountAt,
                                                                                              os.readlink(self.mountAt),
                                                                                              self.pointTo),
                _LINK_ACTION)
            os.remove(self.mountAt)

        # If member exists and its not a link, then we have encountered an error
        if os.path.exists(self.mountAt) and not os.path.islink(self.mountAt):
            log("{} already exists, but it is not a link".format(self.mountAt), _LINK_ACTION)
            raise Exception(
                "Can't mount {} at {}, because {} already exists and its not a link".format(self.pointTo, self.mountAt,
                                                                                            self.mountAt))
            # If we're trying to mount something that doesn't exist, we're again running into an error
        if not os.path.exists(self.pointTo):
            log("Can't point {} to {}, because {} doesn't exist".format(self.mountAt, self.pointTo, self.pointTo),
                _LINK_ACTION)
            raise Exception("Can't mount {} as {}, because it doesn't exist".format(self.pointTo, self.mountAt))

        # If the link doesn't exist, we can finally create it
        if not os.path.exists(self.mountAt) and os.path.exists(self.pointTo):
            self.createLink()

    def createLink(self):
        # Ensure that the parent directory exists
        parent = os.path.dirname(self.mountAt)
        if not os.path.exists(parent):
            os.makedirs(parent)
            # Actually create link
        cmd = 'ln -s {} {}'.format(self.pointTo, self.mountAt)
        status, _ = commands.getstatusoutput(cmd)
        log("Created link from {} to {}".format(self.mountAt, self.pointTo), _LINK_ACTION)
        if not status == 0:
            raise Exception("Failure while creating softlink {} -> {}".format(self.mountAt, self.pointTo))


class RepoInstruction:
    def __init__(self, repo_url, checkout_to, soft_link_instructions=None):
        """
        @type repo_url: str
        @type checkout_to: str
        @type soft_link_instructions: list of SoftLinkInstruction
        """
        self.__repo_url = repo_url
        self.__checkout_to = checkout_to
        if not soft_link_instructions: soft_link_instructions = []
        self.__soft_link_instructions = soft_link_instructions

    @property
    def repoUrl(self):
        return self.__repo_url

    @property
    def checkoutTo(self):
        return self.__checkout_to

    @property
    def softLinkInstructions(self):
        return self.__soft_link_instructions

    def addLinkInstruction(self, instruction):
        self.__soft_link_instructions.append(instruction)

    def updateRepo(self):
        """
        Clones or Updates the repo specified in this instruction
        @rtype : list of git.ChangeObject
        """
        repo = git.Repo(url=self.repoUrl, path=self.checkoutTo)
        changes = repo.cloneOrPull()
        log("Cloned/updated repo {} stored at {}".format(self.repoUrl, self.checkoutTo), _REPO_ACTION)

        return self.__filterChanges(changes)

    def __str__(self):
        return '({} => {}, {})'.format(self.repoUrl, self.checkoutTo, self.__soft_link_instructions)

    def __repr__(self):
        return self.__str__()

    def __filterChanges(self, changes):
        """
        Throws away changes in directories that are not mounted and rewrites paths so that they can be used as in the
        metamodel
        @type changes: list of git.ChangeObject
        """

        def findInstruction(file_path):
            for instr in self.softLinkInstructions:
                if instr.pointTo in file_path:
                    return instr
            return None

        modified_changes = []
        for change in changes:
            sl_instruction = findInstruction(change.path)
            if sl_instruction:
                rewritten_path = change.path.replace(sl_instruction.pointTo,
                                                     sl_instruction.mountAt.replace(const101.sRoot, ''))
                if rewritten_path.startswith('/'): rewritten_path = rewritten_path[1:]
                original_path = change.path
                change.path = rewritten_path
                modified_changes.append(change)
                log("Rewriting {} to {}".format(original_path, rewritten_path), _CHANGE_REWRITE_ACTION)
            else:
                log("Found no instruction for {} - there it can't be important and will be ignored".format(change.path),
                    _CHANGE_REWRITE_ACTION)

        return modified_changes

