import os
from path import Path as path
import subprocess

def generate_tree(directory, prefix=""):

    tree = []
    entries = sorted(os.listdir(directory))  # Sort entries for consistent order

    for index, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = (index == len(entries) - 1)

        if is_last:
            tree.append(f"{prefix}└── {entry}")
            next_prefix = f"{prefix}    "
        else:
            tree.append(f"{prefix}├── {entry}")
            next_prefix = f"{prefix}│   "

        if os.path.isdir(path):
            tree.append(generate_tree(path, next_prefix))
    return "\n".join(tree)

def get_repo(query, repo_url, refresh = False, valid_extensions = [".py", ".md", ".txt"]):
    if repo_url.lower().endswith(".git"):
        repo_url = repo_url[:-4]
    local_repo_dir = str(path(repo_url).name)
    if refresh:
        subprocess.run(["rm","-rf",local_repo_dir])
    if not path(local_repo_dir).exists():
        subprocess.run(["git","clone","repo_url"])
    files_to_open = []
    valid_extensions = set(valid_extensions)
    for f in path(local_repo_dir).walkfiles():
        if f.ext in valid_extensions:
            files_to_open.append(f)
    txt = """
    File structure:
    ---
    {generate_tree(local_repo_dir)}
    ---

    Next, I'll give you the contents of each file in the following section - 
    *************************************************************************

    """
    for f in files_to_open:
        with open(f,'r') as ff:
            contents = ff.read()
        txt += f"""
        {str(f.name)}:
        ---
        {contents}
        ---

        """
    return txt
