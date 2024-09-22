from colorama import Fore, Style

COLUMN_WIDTH_DICT = {
    'rentals': {
        'id': 5,
        'customer': 15,
        'property': 15,
        'period': 10,
        'start_date': 15,
        'end_date': 15,
        'total_price': 20
    },
    'properties': {
        'id': 5,
        'name': 20,
        'type': 10,
        'unit_price': 20,
        'unit_period': 10,
        'address': 30
    },
    'customers': {
        'id': 5,
        'nik': 20,
        'full_name': 20,
        'phone': 20
    }
}

def generate_headers_list(data_name):
    return list(map(lambda item: { 'name': item[0], 'width': item[1] }, COLUMN_WIDTH_DICT[data_name].items()))

HEADERS = {
    'rentals': generate_headers_list('rentals'),
    'customers': generate_headers_list('customers'),
    'properties': generate_headers_list('properties'),
}

def print_currency(value: int):
    return f"Rp. {value:>12,}".replace(",", ".")

def print_header(table_name, color= Fore.CYAN, style= Style.BRIGHT):
    header_string = ""
    top_line = ""
    bottom_line = ""
    headers = HEADERS[table_name]

    for i in range(len(headers)):
        header = headers[i]
        name = str(header['name'])
        top_line += f"{'-' * header['width']}"
        bottom_line += f"{'-' * header['width']}"
        header_string += f"{name.capitalize():<{header['width']}}"
        
        # add separator if not the last column
        # otherwise, add closing table header line
        if i < len(headers) - 1:
            top_line += "-+-"
            bottom_line += "-+-"
            header_string += " | "
        else:
            top_line += "-+"
            bottom_line += "-+"
            header_string += " |"

    print(color + style + top_line)
    print(color + style + header_string)
    print(color + style + bottom_line + Fore.RESET)

def print_table(data: list, table_name= 'rentals', theme = Fore.LIGHTYELLOW_EX):
    current_headers = HEADERS[table_name]
    print_header(table_name=table_name, color=theme)

    for i in range(len(data)):
        printed_row = ""
        current_data = data[i]

        for j in range(len(current_headers)):
            column = current_headers[j]
            col_name = column['name']
            col_width = column['width']
            str_data = current_data[col_name]
        
            printed_row += f"{str_data:<{col_width}} | "

        print(printed_row)

    print(Style.RESET_ALL)