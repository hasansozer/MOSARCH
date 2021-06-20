from pydriller import repository, Repository, ModifiedFile
from itertools import combinations

source_file_extensions = ['.java', '.c', '.cc', '.cpp', 'cxx', '.h']
moduleno = {}

def get_full_paths_for_Java_source_files(file_list):
    full_paths = []
    for f in file_list:
        if f.new_path is not None:
            full_paths.append(f.new_path.split('\\', 1)[0] + f.filename.split('.java', 1)[0])
    return full_paths

def extract_modules(committed_file_list):
    module_count = 0
    for file_list in committed_file_list:
        pair_list = combinations(file_list, 2)
        for m1, m2 in pair_list:
            if m1 not in moduleno:
                moduleno[m1] = module_count
                module_count += 1
            if m2 not in moduleno:
                moduleno[m2] = module_count
                module_count += 1

def extract_module_dependencies(committed_file_list):
    module_count = len(moduleno)
    dsm = [[0 for x in range(module_count)] for y in range(module_count)]
    for file_list in committed_file_list:
        pair_list = combinations(file_list, 2)
        for m1, m2 in pair_list:
            dsm[moduleno[m1]][moduleno[m2]] += 1
            dsm[moduleno[m2]][moduleno[m1]] += 1
    print(dsm)

print("obtaining commits...")
repo = Repository('https://github.com/cdorn/ArchStudio',
                  only_in_branch='master',
                  only_no_merge=True,
                  only_modifications_with_file_types=source_file_extensions)

print("analyzing changed files...")
committed_files = []
for commit in repo.traverse_commits():
    files = commit.modified_files
    changed_files = [m for m in commit.modified_files if m.change_type == m.change_type.MODIFY]
    changed_source_files = [s for s in changed_files if s.filename.endswith(tuple(source_file_extensions))]
    file_list = get_full_paths_for_Java_source_files(changed_source_files)
    if len(file_list) > 1:
        committed_files.append(file_list)

print("extracting modules...")
extract_modules(committed_files)
print("number of modules: {}".format(len(moduleno)))

print("analyzing module dependencies...")
extract_module_dependencies(committed_files)
