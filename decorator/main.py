from decorator.logger import logger

if __name__ == '__main__':

    @logger('log.txt')
    def read_cook_book(file_name):
        cook_book = {}
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
                    recipe.append({'ingredient_name': items[0], 'quantity': int(items[1]), 'measure': items[2]})
                    col -= 1
                    if col == 0:
                        cook_book[name] = recipe
                        name = ''
                        col = 0
                        recipe = []

        return cook_book

    cook_book = read_cook_book('recipes.txt')
    print(cook_book)
