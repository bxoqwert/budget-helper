"""Простые структуры данных для бюджета.

Здесь живут стек для отмены действий и бинарное дерево поиска,
в котором траты лежат по возрастанию суммы.
"""


# Стек работает по правилу последний пришел, первый ушел
class Stack:
    # Создаем пустой стек на основе обычного списка
    def __init__(self):
        self.items = []

    # Кладем элемент на вершину
    def push(self, value):
        self.items.append(value)

    # Снимаем элемент с вершины, а если стек пуст, возвращаем None
    def pop(self):
        if self.items:
            return self.items.pop()
        return None

    # Проверяем, что в стеке ничего нет
    def is_empty(self):
        return len(self.items) == 0


# Один узел дерева хранит целую трату и ссылки на двух детей
class Node:
    # Запоминаем трату, а потомков пока оставляем пустыми
    def __init__(self, expense):
        self.expense = expense
        self.left = None
        self.right = None


# Бинарное дерево поиска, слева меньшие суммы, справа большие или равные
class BudgetTree:
    # Создаем пустое дерево без корня
    def __init__(self):
        self.root = None

    # Добавляем трату в дерево
    def add(self, expense):
        self.root = self._add(self.root, expense)

    # Рекурсивно ищем место для новой траты и ставим ее туда
    def _add(self, node, expense):
        if node is None:
            return Node(expense)
        if expense.amount < node.expense.amount:
            node.left = self._add(node.left, expense)
        else:
            node.right = self._add(node.right, expense)
        return node

    # Удаляем из дерева конкретную трату
    def remove(self, expense):
        self.root = self._remove(self.root, expense)

    # Рекурсивно находим узел с нужной тратой и убираем его
    def _remove(self, node, expense):
        if node is None:
            return None
        # Это и есть нужный нам узел
        if node.expense is expense:
            # Если одного ребенка нет, ставим на место узла другого
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Если детей двое, берем самую дешевую трату из правого поддерева
            heir = node.right
            while heir.left is not None:
                heir = heir.left
            node.expense = heir.expense
            node.right = self._remove(node.right, heir.expense)
            return node
        # Идем в ту сторону, где может лежать нужная трата
        if expense.amount < node.expense.amount:
            node.left = self._remove(node.left, expense)
        else:
            node.right = self._remove(node.right, expense)
        return node

    # Собираем все траты по возрастанию суммы
    def sorted_list(self):
        result = []
        self._in_order(self.root, result)
        return result

    # Симметричный обход, сначала левое поддерево, потом узел, потом правое
    def _in_order(self, node, result):
        if node is None:
            return
        self._in_order(node.left, result)
        result.append(node.expense)
        self._in_order(node.right, result)

    # Самая дешевая трата лежит в самом левом узле
    def cheapest(self):
        if self.root is None:
            return None
        node = self.root
        while node.left is not None:
            node = node.left
        return node.expense

    # Самая дорогая трата лежит в самом правом узле
    def most_expensive(self):
        if self.root is None:
            return None
        node = self.root
        while node.right is not None:
            node = node.right
        return node.expense
