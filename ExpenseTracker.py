
from babel.numbers import get_currency_symbol
from pathlib import Path
from datetime import datetime

from src.Interface import Interface
from src.Config import Config
from src.Storage import Storage

# main function for input
def get_option(max_option):
    option = int(input(" +- Option: "))

    # max_option variable to make it more flexible
    if option < 1 or option > max_option:
        raise ValueError

    return option

# just space
def space():
    print("\n"*30)

# options function
def extract_expenses():
    # To make it a little more simple
    def get_expense_id(extract):
        expense_id = str(input(" +- Expense id: "))
        expense = None
        try:
            # get the expense by id
            expense = extract[expense_id]
            return expense
        except KeyError:
            interface.display_invalid_message("Expense not found...")
        return expense

    def edit_expense(expense):
        space()
        interface.display_edit_or_confirm_expense(expense, config.default_month)
        print()

        while True:
            try:
                # ask for confirmation (if is the correct expense)
                confirm = str(input(" +- Confirm [Y/N]: ")).upper()

                # for invalid options
                if confirm != "Y" and confirm != "N":
                    raise ValueError

                if confirm == "N":
                    break
                else:
                    space()
                    interface.display_head_interface()
                    print()

                    # get the symbol by the expense currency and locale
                    symbol = get_currency_symbol(expense['currency'], expense['locale'])
                    # get the new name and the new value
                    new_name = str(input(" +- New name: "))
                    new_value = float(input(f" +- New value: {symbol}"))

                    # sets the new name and new value at the expenses
                    expense['name'] = new_name
                    expense['value'] = f"{new_value:.2f}"

                    # ask for confirmation again
                    space()
                    interface.display_edit_or_confirm_expense(expense, config.default_month)
                    confirm = str(input(" +- Confirm [Y/N]: ")).upper()
                    
                    if confirm != "Y" and confirm != "N":
                        raise ValueError
    
                    if confirm == "N":
                        break
                    else:
                        # return the expense edited
                        return expense
            except ValueError:
                interface.display_invalid_message()
        return None

    # creates a expense file if dont exists
    if not Path(f"{config.expenses_file_path}\\{config.default_month}.json").exists():
        storage.create_expense_file(config.expenses_file_path, config.default_month)

    # get the all the extracts
    extract = storage.get_expense_list(f"{config.expenses_file_path}\\{config.default_month}.json")
    extract_pages = ""

    # turn the extracts into pages
    if len(extract) > 0:
        extract_pages = [list(extract.items())[i:i+10] for i in range(0, len(extract), 10)]

    actual_page = 0
    while True:
        space()
        interface.display_page_interface(extract_pages[actual_page] if extract_pages != "" else "", actual_page, len(extract_pages) - 1 if extract_pages != "" else 0)
        print()

        try:
            option = str(input(" +- Option: ")).lower().strip()

            # prev and next logic
            if (option == "prev" and actual_page == len(extract_pages) - 2)\
            or (option == "next" and actual_page == len(extract_pages) - 1):
                raise ValueError

            match option:
                case "prev": # go back
                    actual_page -= 1
                case "next": # go foward
                    actual_page += 1
                case "x": # exit
                    break
                case "i": # info from the expense
                    if len(extract) > 0:
                        expense = get_expense_id(extract)

                        space()
                        interface.display_expense_info(expense, get_currency_symbol(expense['currency'], expense['locale']))
                    else:
                        interface.display_invalid_message("The file is empty...")
                case "e": # edit
                    # verify if the file is empty
                    if len(extract) > 0:
                        # get the id to edit
                        expense_id = get_expense_id(extract)

                        if expense != None:
                            # calls the edit function
                            expense = edit_expense(expense)

                            if expense != None:
                                # update the expense in the expenses list and save it
                                extract[expense_id] = expense
                                storage.update_expense_json(extract, config.expenses_file_path, config.default_month)

                    else: # shows a message if the file is empty
                        interface.display_invalid_message("The file is empty...")
                case "t":
                    if len(extract) > 0:
                        # creating variables
                        item_quantity = len(extract)
                        info = {}

                        # getting the total for every single currency
                        for expense in extract:
                            # creates a currency if the currency wasnt registred in the list before
                            if not any(extract[expense]['currency'] in info[i]['currency'] for i in info):
                                info |= {
                                    len(info):{
                                        'currency':extract[expense]['currency'],
                                        'locale':extract[expense]['locale'],
                                        'itens_quantity': 0,
                                        'expenses': 0.00
                                    }
                                }
                                
                            # saves the data in the info dict
                            for data in info:
                                if extract[expense]['currency'] == info[data]['currency'] and extract[expense]['locale'] == info[data]['locale']:
                                    info[data]['expenses'] += float(extract[expense]['value'])
                                    info[data]['itens_quantity'] += 1

                        space()
                        interface.display_total_info(info, item_quantity)
                    else: # if the file is empty
                        interface.display_invalid_message("this file is empty...")
                case _: # else
                    raise ValueError
        except ValueError:
            interface.display_invalid_message()

# add another expense at the current month
def add_expenses():
    # verify if the actual expense file path
    if not Path(f"{config.expenses_file_path}\\{config.default_month}.json").is_file():
        # creates a new file
        storage.create_expense_file(config.expenses_file_path, config.default_month)

    space()
    # shows the interface
    interface.display_head_interface()

    # get the symbol
    symbol = get_currency_symbol(config.currency, config.locale)

    while True:
        try:
            value = float(input(f" +- Price: {symbol}"))
            break
        except ValueError:
            # message if the value are NOT a float
            interface.display_invalid_message("Please, insert a valid value")

    name = str(input(" +- Name: "))

    space()
    interface.display_confirm_add(name, f"{value:.2f}", symbol)
    print()

    # loop for confirmation
    while True:
        confirm = str(input(" +- Confirm the values with Y to continue and N for cancel: ")).upper()
        # if Y just save and break
        if confirm == "Y":
            # update the JSON
            storage.create_expense_json(config.currency, config.locale, value, name.capitalize(), f"{config.expenses_file_path}/{config.default_month.lower()}.json", config.default_month)
            break
        # if N just break
        elif confirm == "N":
            break
        # go back to the start of the loop
        else:
            interface.display_invalid_message()

# settings option
def settings():
    # all currencies
    currencies = {
        "BRL": "pt_BR",  # Brazilian Real
        "USD": "en_US",  # US Dollar
        "EUR": "de_DE",  # Euro
        "GBP": "en_GB",  # British Pound
        "JPY": "ja_JP",  # Japanese Yen
        "CNY": "zh_CN",  # Chinese Yuan
        "KRW": "ko_KR",  # South Korean Won
        "CAD": "en_CA",  # Canadian Dollar
        "AUD": "en_AU",  # Australian Dollar
        "CHF": "de_CH",  # Swiss Franc
        "INR": "en_IN",  # Indian Rupee
        "MXN": "es_MX",  # Mexican Peso
        "ARS": "es_AR",  # Argentine Peso
        "CLP": "es_CL",  # Chilean Peso
        "COP": "es_CO",  # Colombian Peso
        "PEN": "es_PE",  # Peruvian Sol
        "ZAR": "en_ZA",  # South African Rand
        "NZD": "en_NZ",  # New Zealand Dollar
        "SEK": "sv_SE",  # Swedish Krona
        "NOK": "nb_NO",  # Norwegian Krone
        "DKK": "da_DK",  # Danish Krone
        "PLN": "pl_PL",  # Polish Zloty
        "TRY": "tr_TR",  # Turkish Lira
        "RUB": "ru_RU",  # Russian Ruble
        "SGD": "en_SG",  # Singapore Dollar
        "HKD": "zh_HK",  # Hong Kong Dollar
        "THB": "th_TH",  # Thai Baht
        "IDR": "id_ID",  # Indonesian Rupiah
        "MYR": "ms_MY",  # Malaysian Ringgit
        "PHP": "en_PH",  # Philippine Peso
        "AED": "ar_AE",  # UAE Dirham
        "SAR": "ar_SA",  # Saudi Riyal
    }
    
    # divide the currency in pages
    currencies_pages = [list(currencies.items())[i:i+10] for i in range(0, len(currencies), 10)]
    actual_page = 0
    while True:
        space()
        interface.display_settings(config)
        print()

        try:
            option = get_option(3)

            if option == 3: # exit
                break

            match option:
                case 1: # change currency
                    while True:
                        # get the actual page
                        currency_page = currencies_pages[actual_page]

                        space()
                        interface.display_page_interface(currency_page, actual_page, len(currencies_pages) - 1, True)
                        print()

                        try:
                            option = str(input(" +- Option: ")).lower().strip()

                            # prev and next logic
                            if (option == "prev" and actual_page == len(currency_page) - 2)\
                            or (option == "next" and actual_page == len(currency_page) - 1):
                                raise ValueError

                            match option:
                                case "prev": # go back
                                    actual_page -= 1
                                case "next": # go foward
                                    actual_page += 1
                                case "x": # exit
                                    break
                                case "s": # select a currency by the ID
                                    currency_id = str(input(" +- Expense id: "))
                                    currency = None

                                    try:
                                        # gets the currency and locale from the page
                                        currency = currency_page[int(currency_id)]
                                    except ValueError:
                                        interface.display_invalid_message()
            
                                    if currency != None:
                                        # get the config data
                                        old_data = storage.get_config_data()

                                        # update the old_data
                                        old_data['currency'] = currency[0]
                                        old_data['locale'] = currency[1]

                                        # update the settings json
                                        storage.update_config_data(old_data)

                                        # load the new config
                                        config.load_config(storage.get_config_data())
                        except ValueError:
                            interface.display_invalid_message()
                case 2: # load other file
                    interface.display_invalid_message("Not working yet...")
                case _: # else
                    interface.display_invalid_message()
        except ValueError:
            interface.display_invalid_message()

# all folders and files verifications
def prepare_folders():
    # verify folders
    if not storage.verify_folders():
        # creates all folders
        storage.create_folders(datetime.now().strftime("%b"))

    # verify if the config file exists
    if not storage.verify_config_json():
        # creates a new config file
        storage.create_settings_json()

# instancing interface
interface = Interface()
config = Config()
storage = Storage()

# verify all folders
prepare_folders()

# Update to the actual month
storage.update_actual_month()

# load config
config.load_config(storage.get_config_data())

while True:
    space()
    interface.display_main_menu()
    print()

    try:
        option = get_option(4)
    except ValueError:
        interface.display_invalid_message()
        continue

    if option == 4:
        break

    match option:
        case 1: # extract
            extract_expenses()
        case 2: # add
            add_expenses()
        case 3: # Settings
            settings()
        case _:
            interface.display_invalid_message()
            