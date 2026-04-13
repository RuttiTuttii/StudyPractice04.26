# Решение лабораторных работ по Python

## Практическая работа №7  
**Разработка функций на Python**

### Файл: `lab7.py`

```python
# практическая 7 - все функции в формате task1, task2 и т.д.

def task1(a: 'число которое возводим в степень' = 2, x: 'степень в которую возводим' = 1):
    """возводит число a в степень x. по умолчанию a = 2"""
    # всё просто через встроенный оператор
    return a ** x


def task2(n: 'число факториал которого считаем'):
    """рекурсивно считает факториал. если данные кривые (строка или отрицательное) — возвращает -1"""
    if not isinstance(n, int) or n < 0:
        return -1
    if n == 0 or n == 1:
        return 1
    return n * task2(n - 1)


def task3(*numbers: 'любое количество чисел через запятую'):
    """выводит сумму, среднее, максимум, минимум и количество всех переданных чисел"""
    if not numbers:
        print("ни одного числа не передали")
        return
    
    total = sum(numbers)
    count = len(numbers)
    avg = total / count
    maximum = max(numbers)
    minimum = min(numbers)
    
    print(f"сумма: {total}")
    print(f"среднее: {avg}")
    print(f"максимум: {maximum}")
    print(f"минимум: {minimum}")
    print(f"количество чисел: {count}")


def task4(lst: 'список который нужно изменить', multiplier: 'на что умножаем каждый элемент' = -1):
    """умножает каждый элемент списка на multiplier. если multiplier не передали — умножает на -1"""
    for i in range(len(lst)):
        lst[i] *= multiplier
    # список меняется прямо по месту, возвращать ничего не надо


# лямбда-функция для 5.5
linear = lambda a, x, b: a * x + b


def task5(names: 'список имён абитуриентов', math: 'баллы по математике', russian: 'баллы по русскому', informatics: 'баллы по информатике'):
    """собирает список кортежей в формате (фио, мат, рус, инф)"""
    result = []
    for i in range(len(names)):
        result.append((names[i], math[i], russian[i], informatics[i]))
    return result
```

Практическая работа №8

Создание и использование модулей на Python

Файл модуля: my_module.py

```python
# мой модуль для практической 8 - функции в формате task1, task2...

def task1(name: 'имя человека' = None):
    """выводит hello, world или hello, имя если передали параметр"""
    if name:
        print(f"hello, {name}")
    else:
        print("hello, world")


def task2(n: 'натуральное число', base: 'основание системы счисления' = 2):
    """рекурсивно переводит число из десятичной в n-ричную систему"""
    if n < 0 or base < 2:
        return "ошибка: число должно быть неотрицательным, основание >= 2"
    if n < base:
        return str(n)
    return task2(n // base, base) + str(n % base)


def task3(text: 'текст который нужно разбить на предложения'):
    """выводит каждое предложение переданного текста с новой строки"""
    import re
    sentences = re.split(r'[.!?]+', text)
    for sentence in sentences:
        cleaned = sentence.strip()
        if cleaned:
            print(cleaned + '.')


def task4(text: 'строка для шифрования', key: 'сдвиг алфавита' = 3):
    """шифрует текст шифром цезаря. работает с русским и английским алфавитом"""
    result = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                alphabet = 'abcdefghijklmnopqrstuvwxyz' if char.isascii() else 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
            else:
                alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if char.isascii() else 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
            idx = alphabet.find(char)
            if idx != -1:
                new_idx = (idx + key) % len(alphabet)
                result += alphabet[new_idx]
            else:
                result += char
        else:
            result += char
    return result


def task5(a: 'первое число', b: 'второе число'):
    """побитовое И (and) с красивым выводом в двоичном виде"""
    res = a & b
    print(f"{a} & {b} = {res}")
    print(f"  {bin(a)[2:].zfill(8)}")
    print(f"& {bin(b)[2:].zfill(8)}")
    print(f"= {bin(res)[2:].zfill(8)}")


def task6(a: 'первое число', b: 'второе число'):
    """побитовое ИЛИ (or)"""
    res = a | b
    print(f"{a} | {b} = {res}")
    print(f"  {bin(a)[2:].zfill(8)}")
    print(f"| {bin(b)[2:].zfill(8)}")
    print(f"= {bin(res)[2:].zfill(8)}")


def task7(a: 'первое число', b: 'второе число'):
    """побитовое исключающее ИЛИ (xor)"""
    res = a ^ b
    print(f"{a} ^ {b} = {res}")
    print(f"  {bin(a)[2:].zfill(8)}")
    print(f"^ {bin(b)[2:].zfill(8)}")
    print(f"= {bin(res)[2:].zfill(8)}")


def task8(a: 'число'):
    """побитовое НЕ (not)"""
    res = ~a
    print(f"~{a} = {res}")
    print(f"  {bin(a)[2:].zfill(8)}")
    print(f"~ → {bin(res)[2:].zfill(8) if res >= 0 else bin(res)[3:].zfill(8)}")


# если модуль запускают напрямую — можно потестировать
if __name__ == "__main__":
    task1("андрей")
    print(task2(255, 16))
```

Файл для тестирования модуля: test_module.py

```python
import my_module

my_module.task1("саша")
print(my_module.task2(42, 2))
my_module.task3("это первое предложение. а это второе! и третье?")
print(my_module.task4("python", 5))
my_module.task5(12, 25)
```

---

Практическая работа №9

Разработка классов на Python

Файл: lab9_classes.py

```python
# практическая 9 - классы (всё в одном файле)

class Author:
    """класс автор с фио и страной"""
    
    def __init__(self, fio: 'фамилия имя отчество', country: 'страна автора'):
        self.fio = fio
        self.country = country
    
    def print_info(self):
        """выводит информацию об авторе"""
        print(f"автор: {self.fio}, страна: {self.country}")


class Book:
    """класс книга"""
    
    def __init__(self, title: 'название книги'):
        """создаёт книгу и сразу сообщает об этом"""
        self.title = title
        self.__content = []          # приватное поле — список произведений
        print(f"книга '{title}' создана")
    
    def __del__(self):
        """сообщает когда книга удаляется"""
        print(f"книга '{self.title}' удалена")
    
    def add_work(self, work_title: 'название произведения'):
        """добавляет произведение в содержание книги"""
        self.__content.append(work_title)
    
    def get_works_count(self):
        """возвращает количество произведений в книге"""
        return len(self.__content)
    
    def print_book_info(self):
        """красиво выводит информацию о книге и её содержании"""
        print(f"книга: {self.title}")
        print("содержание:")
        if not self.__content:
            print("  (пока пусто)")
        else:
            for i, work in enumerate(self.__content, 1):
                print(f"  {i}) {work}")


class AuthorBook(Author, Book):
    """класс книга автора — множественное наследование"""
    
    def __init__(self, fio: 'фио автора', country: 'страна', title: 'название книги'):
        Author.__init__(self, fio, country)
        Book.__init__(self, title)
    
    def print_full_info(self):
        """выводит фио автора, название книги и всё содержание"""
        print(f"автор: {self.fio} ({self.country})")
        self.print_book_info()
```
