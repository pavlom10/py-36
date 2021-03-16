import hashlib

def md5_strings(file_name):
    with open(file_name, "r") as file:
        for line in file:
            yield hashlib.md5(line.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    for line in md5_strings('countries.txt'):
        print(line)