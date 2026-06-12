"""Отчеты по категориям.

Считаем сумму трат по каждой категории и сортируем их вставками,
чтобы самые затратные категории оказались наверху.
"""


# Сортируем вставками так, чтобы большие суммы оказались в начале списка
def insertion_sort(rows):
    for i in range(1, len(rows)):
        current = rows[i]
        j = i - 1
        while j >= 0 and rows[j][1] < current[1]:
            rows[j + 1] = rows[j]
            j -= 1
        rows[j + 1] = current
    return rows


# Считаем сумму и количество трат по каждой категории
def category_totals(expenses):
    totals = {}
    counts = {}
    for expense in expenses:
        name = expense.category
        totals[name] = totals.get(name, 0) + expense.amount
        counts[name] = counts.get(name, 0) + 1
    rows = []
    for name in totals:
        rows.append((name, totals[name], counts[name]))
    return rows


# Возвращаем категории по убыванию суммы трат
def categories_by_spending(expenses):
    rows = category_totals(expenses)
    insertion_sort(rows)
    return rows
