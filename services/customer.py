from utils.common import get_next_id, find_by_id, do_sort, do_search, validate_sort
from utils.print_table import print_table

SORT_FIELD_LIST = ['full_name', 'nik', 'phone']

def is_valid_customer(customer_id, customers: list):
    selected = find_by_id(customer_id, customers)

    if selected is None:
        print(f"\nError: Invalid customer ID={customer_id}. Not found")
        return False
    
    return True

def matches_search(search_key: str, customer: dict):
    cust_name = str(customer['full_name']).lower()
    return search_key in cust_name or search_key in str(customer['nik']) or search_key in str(customer['phone'])

##############################################
# CRUD methods
##############################################
def print_customer_list(customers: list):
    print_table(customers, table_name='customers')

def search_and_sort(customers: list):
    search = input("Please enter value to search, this will be matched on customer's name or phone or NIK (empty will show all records): ")
    sort_by_str= input("Please enter field to be sort on ['full_name'/'name', 'nik', 'phone'], by using following format: name=desc or name=asc: ")

    # use copy list to prevent editing the content when showing search result
    result = customers.copy()
    if search:
        search = search.lower()
        result = do_search(search, result, matches_search)
    
    if sort_by_str:
        is_valid, field, order = validate_sort(sort_by_str, SORT_FIELD_LIST)
        if not is_valid:
            return
        
        result = do_sort(field, order, input_list=result)

    print("-"*50)
    print_customer_list(result)

def add_customer(customers: list):
    new_id = get_next_id(customers)

    name = input("Please input customer full name: ")
    nik = input("Please input customer NIK: ")
    if not nik:
        print("\nError: NIK is mandatory!")
        return

    phone = input("Please input customer phone number: ")

    new_data = {
        "id": new_id,
        "full_name": name,
        "nik": nik,
        "phone": phone
    }

    customers.append(new_data)
    print(f"Customer is successfully added!")

def remove_customer(customers: list):
    id = input("Please select customer ID to remove: ")
    if not id.isdigit():
        print("\nError: Customer ID must be a number!")
        return

    id = int(id)
    is_valid = is_valid_customer(id, customers)
    
    if not is_valid:
        return
    
    customers[:] = list(filter(lambda item: item['id'] != id, customers))
    print(f"Customer ID:{id} is successfully removed!")


    