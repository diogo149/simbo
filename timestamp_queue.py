import os
import time


def try_remove(filename):
    try:
        os.remove(filename)
    except:
        pass


class TimestampQueue(object):

    def __init__(self,
                 folder=".",
                 queue_limit=10):
        self.folder = folder
        self.queue_limit = queue_limit
        try:
            os.mkdir(folder)
        except OSError:
            pass

    def push(self, s):
        self.prune()
        timestamp = int(time.time())
        with open(os.join(self.folder, str(timestamp)), 'w') as outfile:
            outfile.write(s)
        return self

    def pop(self):
        self.prune()
        files = os.listdir(self.folder)
        if len(files) < 1:
            return None
        filename = os.join(self.folder, files[0])
        with open(filename) as infile:
            results = infile.read()
        try_remove(filename)
        return results


    def prune(self):
        if self.queue_limit is not None:
            for filename in os.listdir(self.folder)[:-self.queue_limit]:
                try_remove(os.join(self.folder, filename))
