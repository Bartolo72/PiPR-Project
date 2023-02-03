import json


def create_income_history(clients, file_handle):
    """
    income should be kept in a json flie as well
    data = {
            'individual type': {
                type: <income>,
                }
            'group': <income_for_groups>
            }
    """
    types = [_type.name for _type in clients.individual.types]
    individual_income = {_type: 0 for _type in types}
    income = {
        'individual type': individual_income,
        'group': 0
    }
    json.dump(income, file_handle, indent=4)


def set_income_from(client, price, income):
    """
    client - name of the client type
    used when reservation is confirmed
    """
    if client == 'group':
        income['group'] += int(price)
    else:
        income['individual type'][client] += int(price)


def calculate_income(income):
    result = []
    individual_prices = [int(price) for price in income["individual type"].values()]
    result.append(sum(individual_prices))
    result.append(income['group'])
    return sum(result)


def create_report(date, income):
    """
    income - json file
    date - '<day>/<month>/<year>'
    1. It should take info about all income from specific clients types
    2. Display the income
    """
    types = [_type for _type in income['individual type'].keys()]
    lines = []
    lines.append(f"Date:{date:<20}")
    lines.append(f"{'-'*30}")
    for _type in types:
        type_income = income["individual type"][_type]
        line = f"{_type:<15}{type_income:>15}"
        lines.append(line)
    group_income = income['group']
    lines.append(f"{'group':<15}{group_income:>15}")
    lines.append(f"{'-'*30}")
    full_income = calculate_income(income)
    lines.append(f"Final income: {full_income:>16}")
    report_doc = '\n'.join(lines)
    return report_doc


def display_report(report):
    return print(report)
