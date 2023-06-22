
def read_file_list(file_list):
    try:
        file = open(file_list, 'r')
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}: {file_list}")
        return None

    lines = file.readlines()
    if len(lines) < 1:
        print(f"Could not read from {file_list}")
        return

    samples = []
    for line in lines:
        ls = line.strip()
        samples.append(ls)
    return samples
