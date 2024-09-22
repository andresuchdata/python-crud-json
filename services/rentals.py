from utils.date import get_period, validate_and_generate_date, is_date_format
from utils.common import get_next_id, find_by_id, do_search, do_sort, validate_sort
from utils.print_table import print_table
from services.property import print_property_list
from services.customer import print_customer_list

VALID_FIELDS_EDIT = [
    'property', 'customer', 'start_date', 'end_date'
]
SORT_FIELD_LIST = ['start_date', 'end_date', 'total_price']

##############################################
# Utilities
##############################################
def is_valid_field(field):
    for item in VALID_FIELDS_EDIT:
        if item == field:
            return True

    return False

def is_property_taken(property_id, rentals: list):
    for rent in rentals:
        if rent['property'] == property_id:
            return True

    return False

def is_valid_customer(customer_id, customers: list):
    selected = None

    for item in customers:
        if item['id'] == customer_id:
            selected = item
            break

    if selected is None:
        print(f"\nError: Invalid customer {customer_id}. Not found")
        return False
    
    return True

def validate_and_get_property(property_id: int, properties: list, rentals: list):
    property_selected = None
    
    for prop in properties:
        if prop['id'] == property_id:
            property_selected = prop
            break

    if property_selected is None:
        print(f"\nError: Invalid property {property_id}. Not found")
        return False, property_selected
    
    if property_selected and is_property_taken(property_id, rentals):
        print(f"\nProperty (ID: {property_id}) is in active rental. Please select another property!")
        return False, property_selected

    return True, property_selected

def is_validate_rental(id: int, rentals: list) -> tuple:
    found_rental = find_by_id(id, rentals)
    is_valid = True

    if found_rental is None:
        print(f"\nError: Rental ID {id} is not found")
        is_valid = False

    return is_valid, found_rental

def calculate_total_price(unit_price: int, period: float):
    return unit_price * period

def match_rental(search_key: str, rental: dict):
    customer_name = str(rental['customer']).lower()
    property_name = str(rental['property']).lower()

    return search_key in customer_name or search_key in property_name

def populate_customer_property_info(rentals: list, customers: list, properties: list):
    result = []
    # get all customer names in a dict
    customer_dict = {}
    properties_dict = {}
    for cust in customers:
        customer_dict[cust['id']] = cust
    
    for prop in properties:
        properties_dict[prop['id']] = prop
    
    # copy each dictionary in rentals list, to avoid mutating the property and customer ID data
    for rent in rentals:
        new_rental = rent.copy()
        current_prop = properties_dict[rent['property']]
        new_rental['customer'] = customer_dict[rent['customer']]['full_name']
        new_rental['property'] = properties_dict[rent['property']]['name']

        # populate period with unit time (days, months, or years)
        new_rental['period'] = f"{rent['period']} {current_prop['unit_period']}"

        result.append(new_rental)

    return result

##############################################
# CRUD methods
##############################################
def print_rental_list(rentals: list, properties: list, customers: list):
    result = populate_customer_property_info(rentals, customers, properties)
    print_table(result, table_name='rentals')

def search_sort_rental(rentals: list, customers: list, properties: list):
    search = input("Please enter value to search, this will be matched on rental's customer name or property name (empty will show all records): ")
    sort_by_str= input(f"Please enter field to be sort on {SORT_FIELD_LIST}, by using following format: name=desc or name=asc: ")

    result = populate_customer_property_info(rentals, customers, properties)

    if search:
        search = search.lower()
        result = do_search(search, result, match_rental)
    
    if sort_by_str:
        is_valid, field, order = validate_sort(sort_by_str, SORT_FIELD_LIST)
        if not is_valid:
            return
        
        result = do_sort(field, order, input_list=result)

    print("-"*50)
    print_table(result, table_name='rentals')
   
def add_rental(rentals: list, properties: list, customers: list):
    print_property_list(properties)
    property_id = input("\nPlease the property ID for rent: ")
    if not property_id.isdigit():
        print("\nError: Property ID must be a number!")
        return
    
    property_id = int(property_id)
    is_valid, selected_property = validate_and_get_property(property_id, properties, rentals)

    if not is_valid:
        return

    print_customer_list(customers)
    customer_id = input("\nPlease the customer ID for rent: ")
    if not customer_id.isdigit():
        print("\nError: Customer ID must be a number!")
        return
    
    customer_id = int(customer_id)
    is_valid = is_valid_customer(customer_id, customers)

    if not is_valid:
        return

    start_str = input("Please input start date of the rent - format DD/MM/YYYY: ")
    is_valid = is_date_format(start_str)
    if not is_valid:
        print(f"\nDate {start_str} is not in format DD/MM/YYYY")
        return
    
    end_str = input("Please input end date of the rent - format DD/MM/YYYY: ")    
    is_valid = is_date_format(end_str)
    if not is_valid:
        print(f"\nDate {end_str} is not in format DD/MM/YYYY")
        return


    new_id = get_next_id(rentals)

    # use default 1 id in case new list
    if new_id == -1:
        new_id = 1
    
    # get period
    start_date, is_valid = validate_and_generate_date(start_str)
    if not is_valid:
        return

    end_date, is_valid = validate_and_generate_date(end_str)
    if not is_valid:
        return
    
    period = get_period(start_date, end_date, selected_property['unit_period'])
    period = round(period)
    total_price = calculate_total_price(unit_price=selected_property['unit_price'], period=period)
    
    new_rental = {
        "id": new_id,
        "customer": customer_id,
        "property": property_id,
        "start_date": start_date.strftime("%d/%m/%Y"),
        "end_date": end_date.strftime("%d/%m/%Y"),
        "period": period,
        "total_price": round(total_price)
    }

    rentals.append(new_rental)
    print("New rental has been created successfully!\nPlease select print rental option in main menu")

def edit_rental(rentals: list, properties: list, customers: list):
    rental_id = input("Please select rental ID to edit: ")
    if not rental_id.isdigit():
        print("\nError: Rental ID must be a number!")
        return

    rental_id = int(rental_id)
    is_valid_rental, selected_rental = is_validate_rental(rental_id, rentals)
    
    if not is_valid_rental:
        return

    field = input("Please enter the field to edit ('customer', 'property', 'start_date', 'end_date'): ")
    field = field.lower()

    if is_valid_field(field) is False:
        print("\nError: Invalid field to edit!")
        return
    
    new_value = ""
    if field == 'customer' or field == 'property':
        new_value = input(f"Please enter new data for '{field}' : ")
        if not new_value.isdigit():
            print(f"Error: {field} must be a number!")
            return

        new_value = int(new_value)

        if field == 'property':
            is_valid = validate_and_get_property(new_value, properties, rentals)
            if not is_valid:
                return
        elif field == 'customer':
            if not is_valid_customer(new_value, customers):
                return

        new_entry = {
            field: int(new_value),
        }
        selected_rental.update(new_entry)
    else:
        if field == 'start_date' or field == 'end_date':
            new_value = input(f"Please enter new date for '{field}' (format DD/MM/YYYY): ")
            if not is_date_format(new_value):
                print("\nError: Please use DD/MM/YYYY format!")
                return
        
        new_entry = {
            field: new_value
        }
        selected_rental.update(new_entry)

    print("Successfully updated!")

def remove_rental(rentals: list):
    rental_id = input("Please select rental ID to remove: ")
    if not rental_id.isdigit():
        print("\nError: Rental ID must be a number!")
        return

    rental_id = int(rental_id)
    is_valid_rental, _ = is_validate_rental(rental_id, rentals)
    
    if not is_valid_rental:
        return
    
    # the remove is updated on the original list
    rentals[:] = list(filter(lambda item: item['id'] != rental_id, rentals))
    print(f"Rental ID {rental_id} is successfully removed!")


    