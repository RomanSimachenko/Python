def check_relation(net: tuple, first: str, second: str) -> bool:
    contacts = {}

    for name1, name2 in net:
        if name1 in contacts:
            if name2 not in contacts[name1]:
                contacts[name1].append(name2)
        else:
            contacts[name1] = [name2]

        if name2 in contacts:
            if name1 not in contacts[name2]:
                contacts[name2].append(name1)
        else:
            contacts[name2] = [name1]

    contacts_now = [first]
    processed = []

    while contacts_now:
        if second in contacts_now:
            return True

        tmp = []

        for name in contacts_now:
            processed.append(name)

            for name2 in contacts[name]:
                if name2 not in processed:
                    tmp.append(name2)

        contacts_now = tmp
    else:
        return False
    



if __name__ == '__main__':
    net = (
        ("Ваня", "Лёша"), ("Лёша", "Катя"),
        ("Ваня", "Катя"), ("Вова", "Катя"),
        ("Лёша", "Лена"), ("Оля", "Петя"),
        ("Стёпа", "Оля"), ("Оля", "Настя"),
        ("Настя", "Дима"), ("Дима", "Маша")
    )

    assert check_relation(net, "Петя", "Стёпа") is True
    assert check_relation(net, "Маша", "Петя") is True
    assert check_relation(net, "Ваня", "Дима") is False
    assert check_relation(net, "Лёша", "Настя") is False
    assert check_relation(net, "Стёпа", "Маша") is True
    assert check_relation(net, "Лена", "Маша") is False
    assert check_relation(net, "Вова", "Лена") is True
