"""Главный модуль бюджета.

Класс Budget хранит все траты за месяц и отвечает на вопросы о них.
Тут же лежат префиксные суммы, линейный поиск дня максимума и отмена через стек.
"""

from structures import Stack, BudgetTree

DAYS = 31  # Сколько дней в месяце мы учитываем


# Одна трата с днем, суммой и категорией
class Expense:
    # Запоминаем данные одной траты
    def __init__(self, day, amount, category):
        self.day = day
        self.amount = amount
        self.category = category

    # Собираем короткую строку для вывода на экран
    def text(self):
        return "день " + str(self.day) + ", " + str(self.amount) + " руб, " + self.category


# Бюджет за месяц связывает между собой все структуры данных
class Budget:
    # Готовим пустые списки, массивы, дерево и стек
    def __init__(self):
        self.expenses = []                 # Все траты в порядке добавления
        self.per_day = [0] * (DAYS + 1)    # Сумма трат за каждый день, день ноль не используем
        self.prefix = [0] * (DAYS + 1)     # Префиксные суммы, считаем их по запросу
        self.prefix_ready = False          # Верны ли сейчас префиксные суммы
        self.tree = BudgetTree()           # Дерево всех трат по возрастанию суммы
        self.history = Stack()             # Стек добавленных трат для отмены

    # Добавляем новую трату сразу во все структуры
    def add(self, day, amount, category):
        expense = Expense(day, amount, category)
        self.expenses.append(expense)
        self.per_day[day] += amount
        self.tree.add(expense)
        self.history.push(expense)
        self.prefix_ready = False          # Данные поменялись, старые префиксы больше не годятся
        return expense

    # Отменяем последнюю добавленную трату
    def undo(self):
        last = self.history.pop()
        if last is None:
            return None
        self.expenses.remove(last)
        self.per_day[last.day] -= last.amount
        self.tree.remove(last)             # Убираем эту трату из дерева
        self.prefix_ready = False
        return last

    # Считаем префиксные суммы по дням
    def _build_prefix(self):
        # В prefix[i] лежит сумма трат с первого дня по день i
        for i in range(1, DAYS + 1):
            self.prefix[i] = self.prefix[i - 1] + self.per_day[i]
        self.prefix_ready = True

    # Возвращаем сумму трат за период с дня a по день b за O(1)
    def period_sum(self, a, b):
        if not self.prefix_ready:
            self._build_prefix()
        return self.prefix[b] - self.prefix[a - 1]

    # Линейным поиском находим день, в который потрачено больше всего
    def peak_day(self):
        best_day = 1
        for day in range(1, DAYS + 1):
            if self.per_day[day] > self.per_day[best_day]:
                best_day = day
        return best_day, self.per_day[best_day]

    # Считаем, сколько всего потрачено за месяц
    def total(self):
        result = 0
        for expense in self.expenses:
            result += expense.amount
        return result

    # Считаем средний расход, учитывая только дни с тратами
    def average_per_active_day(self):
        active_days = 0
        for day in range(1, DAYS + 1):
            if self.per_day[day] > 0:
                active_days += 1
        if active_days == 0:
            return 0
        return self.total() / active_days
