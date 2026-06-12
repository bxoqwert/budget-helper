"""Консольное меню бюджета.

Запускаем main, выбираем команды по номеру и смотрим результат.
"""

from budget import Budget, DAYS
from reports import categories_by_spending


MENU = (
    "\n=== Бюджет на месяц ===\n"
    "1. Добавить трату\n"
    "2. Отменить последнюю трату\n"
    "3. Сумма за период\n"
    "4. Самый дорогой день\n"
    "5. Итого за месяц\n"
    "6. Категории по сумме трат\n"
    "7. Все траты по возрастанию суммы\n"
    "8. Самая дорогая и самая дешевая трата\n"
    "9. Траты по дням\n"
    "10. Показать список команд\n"
    "0. Выход"
)


# Читаем целое число в нужных границах и повторяем запрос при ошибке
def read_number(prompt, low, high):
    while True:
        text = input(prompt).strip()
        if text.isdigit() and low <= int(text) <= high:
            return int(text)
        print("Нужно целое число от", low, "до", high)


# Спрашиваем данные новой траты и добавляем ее
def do_add(budget):
    day = read_number("День от 1 до " + str(DAYS) + ": ", 1, DAYS)
    amount = read_number("Сумма: ", 1, 1000000000)
    category = input("Категория: ").strip()
    if category == "":
        category = "без категории"
    budget.add(day, amount, category)
    print("Трата добавлена")


# Отменяем последнюю добавленную трату
def do_undo(budget):
    last = budget.undo()
    if last is None:
        print("Отменять нечего")
    else:
        print("Убрали трату " + last.text())


# Считаем сумму трат за выбранный период
def do_period(budget):
    a = read_number("День A: ", 1, DAYS)
    b = read_number("День B: ", 1, DAYS)
    if a > b:
        a, b = b, a   # Дни можно вводить в любом порядке
    print("С дня", a, "по день", b, "потрачено", budget.period_sum(a, b), "руб")


# Показываем день, в который потрачено больше всего
def do_peak(budget):
    day, amount = budget.peak_day()
    if amount == 0:
        print("Трат пока нет")
    else:
        print("Больше всего потрачено в день", day, "на сумму", amount, "руб")


# Показываем итог за месяц и средний расход за день
def do_total(budget):
    if not budget.expenses:
        print("Трат пока нет")
        return
    print("Всего за месяц", budget.total(), "руб")
    print("В среднем за день с тратами", round(budget.average_per_active_day()), "руб")


# Выводим категории, отсортированные по сумме трат
def do_categories(budget):
    rows = categories_by_spending(budget.expenses)
    if not rows:
        print("Трат пока нет")
        return
    print("Категории по сумме трат")
    for name, total, count in rows:
        print(" ", name, total, "руб, трат", count)


# Выводим все траты по возрастанию суммы из дерева
def do_tree(budget):
    rows = budget.tree.sorted_list()
    if not rows:
        print("Трат пока нет")
        return
    print("Траты по возрастанию суммы")
    for expense in rows:
        print("  " + expense.text())


# Показываем самую дорогую и самую дешевую трату
def do_min_max(budget):
    cheap = budget.tree.cheapest()
    pricey = budget.tree.most_expensive()
    if cheap is None:
        print("Трат пока нет")
        return
    print("Самая дешевая трата  " + cheap.text())
    print("Самая дорогая трата  " + pricey.text())


# Выводим сумму трат по каждому дню, где они были
def do_by_day(budget):
    found = False
    print("Траты по дням")
    for day in range(1, DAYS + 1):
        if budget.per_day[day] > 0:
            print("  день", day, budget.per_day[day], "руб")
            found = True
    if not found:
        print("  трат пока нет")


# Загружаем несколько готовых трат для примера
def load_demo(budget):
    demo = [
        (2, 350, "еда"),
        (2, 90, "проезд"),
        (4, 250, "кофе"),
        (5, 1500, "книги"),
        (9, 200, "проезд"),
        (12, 700, "подписки"),
        (14, 3200, "одежда"),
        (16, 480, "еда"),
        (21, 600, "спорт"),
        (27, 900, "кафе"),
    ]
    for day, amount, category in demo:
        budget.add(day, amount, category)


# Запускаем программу и главный цикл меню
def main():
    budget = Budget()
    answer = input("Загрузить примеры трат? (да/нет): ").strip().lower()
    if answer == "да":
        load_demo(budget)
        print("Загружено трат", len(budget.expenses))
    print(MENU)
    while True:
        choice = input("Команда: ").strip()
        if choice == "0":
            print("Выход")
            break
        elif choice == "1":
            do_add(budget)
        elif choice == "2":
            do_undo(budget)
        elif choice == "3":
            do_period(budget)
        elif choice == "4":
            do_peak(budget)
        elif choice == "5":
            do_total(budget)
        elif choice == "6":
            do_categories(budget)
        elif choice == "7":
            do_tree(budget)
        elif choice == "8":
            do_min_max(budget)
        elif choice == "9":
            do_by_day(budget)
        elif choice == "10":
            print(MENU)
        else:
            print("Нет такой команды")


if __name__ == "__main__":
    main()
