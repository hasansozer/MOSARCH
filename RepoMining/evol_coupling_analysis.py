from pydriller import repository, Repository, ModifiedFile

source_file_extensions = ['.java', '.c', '.cc', '.cpp', '.h']

repo = Repository('https://github.com/cdorn/ArchStudio',
                  only_in_branch='master',
                  only_no_merge=True,
                  only_modifications_with_file_types=source_file_extensions)

def get_source_files(file_list):
    return [s for s in file_list if s.filename.endswith(tuple(source_file_extensions))]

def get_full_paths(file_list):
    full_paths = []
    for f in file_list:
        path = f.new_path
        if path is not None:
            full_paths.append(path.split('\\', 1)[0] + f.filename.split('.java', 1)[0])
    return full_paths

for commit in repo.traverse_commits():
    files = commit.modified_files
    changed_files = [m for m in commit.modified_files if m.change_type == m.change_type.MODIFY]
    changed_source_files = get_source_files(changed_files)
    file_list = get_full_paths(changed_source_files)
    print(file_list)