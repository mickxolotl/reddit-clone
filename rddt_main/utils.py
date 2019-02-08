plural_form_cases = (2, 0, 1, 1, 1, 2)


def plural_form(n, forms):
    """Функция возвращает число и просклонённое слово после него
    plural_form(difference.days, ("день", "дня", "дней"))
    """
    form = forms[2 if (4 < n % 100 < 20) else plural_form_cases[min(n % 10, 5)]]

    return f"{n}  {form}"
