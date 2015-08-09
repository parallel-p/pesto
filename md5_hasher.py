import hashlib


def _md5_update(md5, filename):
    with open(filename, "rb") as file:
        md5.update(file.read())


def get_hash(input_data_filename, output_data_filename):
    md5 = hashlib.md5()
    _md5_update(md5, input_data_filename)
    _md5_update(md5, output_data_filename)
    return md5.hexdigest()

