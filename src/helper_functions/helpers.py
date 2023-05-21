def read_file_as_str(filename):
    """Return the read data from input file

    Args:
        filename (_type_): input file

    Returns:
        _type_: return data
    """
    with open(filename, "r") as file:
        data = file.read()
    return data
