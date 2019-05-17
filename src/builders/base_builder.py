from os import listdir
from os.path import isfile, join


class BaseBuilder:

    def __init__(self):
        self.files = []

    def run(self, *args, **kwargs):
        pass

    def load_files(self, input_dir_path):
        self.files = self.get_file_paths(input_dir_path)
        self.files.sort()

    def build(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):
        pass

    @staticmethod
    def get_file_paths(input_dir_path):
        return [
            join(input_dir_path, f)
            for f in listdir(input_dir_path)
            if isfile(join(input_dir_path, f))
        ]
