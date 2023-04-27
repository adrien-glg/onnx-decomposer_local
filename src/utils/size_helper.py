# calculate file size in KB, MB, GB
def convert_bytes(size):
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, unit)
        size /= 1024.0


def get_pretty_size(size):
    pretty_size = convert_bytes(size)
    return pretty_size


def get_pretty_sizes(sizes):
    pretty_sizes = []

    for i in range(len(sizes)):
        pretty_sizes += [convert_bytes(sizes[i])]

    return pretty_sizes
