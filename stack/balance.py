class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def is_string_balanced(string):
    stack = Stack()
    open = ['(', '{', '[']
    close = [')', '}', ']']

    for char in string:
        if char in open:
            stack.push(char)
        elif char in close:
            if stack.size() == 0:
                return False
            last_char = stack.pop()
            if last_char != open[close.index(char)]:
                return False

    return stack.isEmpty()


if __name__ == '__main__':
    string = input('Строка: ')
    if is_string_balanced(string):
        print('Сбалансированно')
    else:
        print('Несбалансированно')

