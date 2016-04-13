
def get_file_text(filename):
    with open(filename, 'r') as f:
        return f.read().replace('\n', '')
