from utils.common import get_next_id, find_by_id, do_sort, do_search, validate_sort
from utils.print_table import print_table

PROPERTY_TYPE = ['land', 'house', 'room']
UNIT_PERIOD = ['days', 'months', 'years']
SORT_FIELD_LIST = ['name', 'type', 'unit_price', 'unit_period']

def is_valid_property(id, properties: list):
    selected = find_by_id(id, properties)

    if selected is None:
        print(f"\nError: Invalid property ID={id}. Not found")
        return False
    
    return True

def match_property(search_key: str, property: dict):
    name = str(property['name']).lower()
    address = str(property['address']).lower()

    return search_key in name or search_key in address

##############################################
# CRUD methods
##############################################
def print_property_list(properties: list):
    print_table(properties, table_name='properties')

def search_and_sort(properties: list):
    search = input("Please enter value to search, this will be matched on property's name or address (empty will show all records): ")
    sort_by_str= input(f"Please enter field to be sort on {SORT_FIELD_LIST}, by using following format: name=desc or name=asc: ")

    # use copy list to prevent editing the content when showing search result
    result = properties.copy()
    if search:
        search = search.lower()
        result = do_search(search, result, logic_function=match_property)
    
    if sort_by_str:
        is_valid, field, order = validate_sort(sort_by_str, SORT_FIELD_LIST)
        if not is_valid:
            return
        
        result = do_sort(field, order, input_list=result)

    print("-"*50)
    print_property_list(result)

def add_property(properties: list):
    new_id = get_next_id(properties)

    name = input("Please input property name (summary): ")
    type = input("Please input type ('land' or 'house' or 'room'): ")
    if not type in PROPERTY_TYPE:
        print(f"\nError: type {type} is not valid. Please use following {PROPERTY_TYPE}!")
        return

    unit_price = input("Please input unit price: ")
    if not unit_price:
        unit_price = 0

    unit_period = input("Please input unit period ('months' or 'years' or 'days' - empty will be 'days'): ")
    if not type in UNIT_PERIOD:
        print(f"\nError: unit_period {type} is not valid. Please use following {UNIT_PERIOD}!")
        return

    new_data = {
        "id": new_id,
        "name": name,
        "type": type,
        "unit_price": unit_price,
        "unit_period": unit_period,
    }

    properties.append(new_data)
    print(f"Property is successfully added!")

def remove_property(properties: list):
    id = input("Please select property ID to remove: ")
    if not id.isdigit():
        print("\nError: Property ID must be a number!")
        return

    id = int(id)
    is_valid = is_valid_property(id, properties)
    
    if not is_valid:
        return
    
    properties[:] = list(filter(lambda item: item['id'] != id, properties))
    print(f"Property ID:{id} is successfully removed!")


    