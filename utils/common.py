import re
ORDER_TYPES = ['asc', 'desc']

# Increment the ID from max available ID in common list
# common_list format must be array of dictionary
# with item MUST have field 'id'
def get_next_id(common_list: list):
    max_id = -1
    
    if len(common_list) > 0:
        max_id = common_list[0]['id']

        for r in range(1,len(common_list)):
            if max_id < common_list[r]['id']:
                max_id = common_list[r]['id']

    return max_id + 1

# Find the item in common_list, based on ID
# common_list format must be array of dictionary
# with item MUST have field 'id'
def find_by_id(id: int, common_list: list) -> dict:
    for item in common_list:
        if item['id'] == id:
            return item

    return None

def do_sort(field: str, order: str, input_list: list) -> list:
    reverse = True if order == 'desc' else False

    return sorted(input_list, key=lambda x: x[field], reverse=reverse)

def do_search(search: str, target_list: list, logic_function: callable) -> list:
    clist = list(filter( lambda item: logic_function(search, item), target_list))
    
    return clist

# validate the sort param to have following format: field=asc or field=desc
def validate_sort(param: str, sort_fields: list) -> tuple:
    field = ''
    order = ''

    pattern = r'^[a-zA-Z_]+=(asc|desc)$'
    if not re.match(pattern, param):
        print("\nInvalid sort param, must be field=desc or field=asc")
        return False, field, order
    
    field, order = param.split('=')
    field = field.lower()
    order = order.lower()
    
    if not field in sort_fields:
        print(f"\nField value must from: {sort_fields}");
        return False, field, order

    # handling when user input: filed== or field=
    if not order or order not in ORDER_TYPES:
        print("\nMust have order from following values: [asc, desc]!");
        return False, field, order
    
    return True, field, order