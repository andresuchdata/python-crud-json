import os
from colorama import Fore
from utils.db import read_db
from utils.print_menu import print_menu
from services.rentals import print_rental_list, add_rental, edit_rental, remove_rental, search_sort_rental
from services.customer import print_customer_list, add_customer, remove_customer, search_and_sort as search_sort_customer
from services.property import print_property_list, add_property, remove_property, search_and_sort as search_sort_property

CUSTOMERS_DB_FILE = os.path.join(os.path.dirname(__file__), 'db', 'customers.json')
PROPERTIES_DB_FILE = os.path.join(os.path.dirname(__file__), 'db', 'properties.json')
RENTALS_DB_FILE = os.path.join(os.path.dirname(__file__), 'db', 'rentals.json')

rentals = list(read_db(RENTALS_DB_FILE))
properties = list(read_db(PROPERTIES_DB_FILE))
customers = list(read_db(CUSTOMERS_DB_FILE))

option = ''

while option.startswith('q') == False:
    print_menu()

    option = input("Please pick any option, or press quit or q to quite the program: ")
    option = option.lower()

    if option == '1':
        print_rental_list(rentals, properties, customers)
    elif option == '2':
        add_rental(rentals, properties, customers)
    elif option == '3':
        edit_rental(rentals, properties, customers)
    elif option == '4':
        remove_rental(rentals)
    elif option == '5':
        search_sort_rental(rentals, customers, properties)
    elif option == '6':
        print_customer_list(customers)
    elif option == '7':
        add_customer(customers)
    elif option == '8':
        remove_customer(customers)
    elif option == '9':
        search_sort_customer(customers)
    elif option == '10':
        print_property_list(properties)
    elif option == '11':
        add_property(properties)
    elif option == '12':
        remove_property(properties)
    elif option == '13':
        search_sort_property(properties)
    elif option == 'q' or option == 'quit':
        continue
    else:
        print("\n")
        print(Fore.RED + "INVALID option! Please try again")
        print()

