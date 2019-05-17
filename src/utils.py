import os

from src.constants import INPUT_DIR_PATH


def split_file(input_file_path, result_dir_path, n):
    file_name = os.path.splitext(input_file_path)[0]
    new_files = [
        os.path.join(result_dir_path, '{}_{}.txt'.format(file_name, i))
        for i in range(1, n+1)
    ]
    chunk_size = os.path.getsize(input_file_path) // n
    with open(input_file_path, 'r') as f:
        for _file in new_files:
            data = f.read(chunk_size)
            nf = open(_file, 'w')
            nf.write(data)
            nf.close()


def get_split_file_path_by_name(name):
    return os.path.join(INPUT_DIR_PATH, name)


# split_file(
#     '/Users/rickskyy/projects/distributed_systems_course/resources/bible.txt',
#     '/Users/rickskyy/projects/distributed_systems_course/resources',
#     15
# )
