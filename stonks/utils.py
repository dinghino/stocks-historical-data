def path_contains_filename(path):
    extensions = ['.csv', '.txt']
    for ext in extensions:
        if path.endswith(ext):
            return True
    return False
