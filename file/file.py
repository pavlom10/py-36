def read_cook_book(file_name):
    name = ''
    col = 0
    recipe = []

    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()

            if line == '':
                pass
            elif name == '':
                name = line
            elif col == 0:
                col = int(line)
            else:
                items = line.split(' | ')
                recipe.append({'ingredient_name': items[0], 'quantity': items[1], 'measure': items[2]})
                col -= 1
                if col == 0:
                    cook_book[name] = recipe
                    name = ''
                    col = 0
                    recipe = []

cook_book = read_cook_book('recipes.txt')
print(cook_book)

#
# with open('recipes.txt', 'r') as f:
#
# with open('test.txt', 'r') as f:
#     print(f.read())
#
# file_path = os.path.join(os.getcwd(), 'text.txt')
#
# with open('test.txt', 'r') as f:
#     print(f.read())
#
# # print(os.getcwd())
#
# #
# # data = f.read()
# # print(data)
# #
# # f.close()
# # print(type(f))