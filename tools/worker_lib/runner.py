from git import Repo

def convert_diff(diff):
    file_1 = diff.a_path
    file_2 = diff.b_path

    if diff.a_mode == 0 and diff.a_blob is None:
        return { 'type': 'DELETED_FILE', 'file': file_2 }

    elif diff.b_mode == 0 and diff.b_blob is None:
        return { 'type': 'NEW_FILE', 'file': file_1 }

    else:
        return { 'type': 'FILE_CHANGED', 'file': file_1 }

class Runner(object):

    def __init__(self, env):
        self.env = env
        self.repo = Repo(self.env['repo101dir'])

    def pull_repo(self):
        base_commit = self.repo.head.commit.hexsha
        info = self.repo.remotes.origin.pull('master')[0]
        diffs = info.commit.diff(base_commit)
        return map(lambda diff: convert_diff(diff), diffs)

    def checkout_commit(self, commit):
        self.repo.git.checkout(commit)

    def history(self, commit):
        return self.repo.iter_commits(commit)
