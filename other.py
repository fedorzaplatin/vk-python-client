import time


def action_date(date):
    """Получает время в формате unixtime, преобразует его и возвращает строку"""
    date = time.gmtime(date + abs(time.timezone))
    today = time.gmtime(time.time())

    if date[0] == today[0] and date[1] == today[1] and date[2] == today[2]:
        string = 'Сегодня '
    elif date[0] == today[0] and date[1] == today[1] and date[2] == today[2] - 1:
        string = 'Вчера '
    elif date[0] == today[0]:
        string = str(date[2]) + ' ' + time.strftime('%B', date) + ' '
    else:
        string = str(date[2]) + ' ' + time.strftime('%B', date) + str(date[0]) + ' '

    string = string + 'в ' + time.strftime('%H:%M', date)
    return string


def select(maximum):
    """Выбор номера из списка. Вынесено в отдельную функцию т.к. часто используется в разных местах кода"""
    num = -1
    while num < 1 or num > maximum:
        num = int(input('Выберите: '))
        if num == maximum:
            return maximum
        elif num < 1 or num > maximum:
            print('Неправильный номер!')
    return num
