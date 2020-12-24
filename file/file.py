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

#task 2
def get_shop_list_by_dishes(dishes, person_count):
    shop_list = {}
    for dish in dishes:
        if dish in cook_book:
            recipe = cook_book[dish]
            for product in recipe:
                name = product['ingredient_name']
                if name in shop_list:
                    shop_list[name]['quantity'] += product['quantity'] * person_count
                else:
                    shop_list[name] = {'measure': product['measure'], 'quantity': product['quantity'] * person_count}

    return shop_list

shop_list = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2)
print(shop_list)


