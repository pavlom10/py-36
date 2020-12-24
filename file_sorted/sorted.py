file_names = ['1.txt', '2.txt', '3.txt']
result_file_name = 'sorted.txt'

def sort_files(file_names, result_file_name):
    file_length = {}
    file_text = {}

    for file_name in file_names:
        with open(file_name, 'r') as f:
            text = f.readlines()
            file_length[file_name] = len(text)
            file_text[file_name] = text

    sorted_file_length = sorted(file_length, key=file_length.get, reverse=True)

    f = open(result_file_name, 'w')
    with open(result_file_name, 'a') as f:
        for file_name in sorted_file_length:
            f.write(file_name)
            f.write('\n')
            f.write(str(file_length[file_name]))
            f.write('\n')
            for line in file_text[file_name]:
                f.write(line)
            f.write('\n')

sort_files(file_names, result_file_name)


