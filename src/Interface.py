from babel.numbers import get_currency_symbol

class Interface():
    def __init__(self):
        self.interface_size = 44

    # interface parts
    def display_head_interface(self):
        print("+" + "-"*self.interface_size + "+")
        print(f"| {'EXPENSE TRACKER':^{self.interface_size-2}} |")
        print("+" + "-"*self.interface_size + "+")

    # display functions
    def display_main_menu(self):
        self.display_head_interface()
        print("| " + " "*(self.interface_size-2) + " |")
        print(f"| {'1. Extract':<{self.interface_size-2}} |")
        print(f"| {'2. Add':<{self.interface_size-2}} |")
        print(f"| {'3. Settings':<{self.interface_size-2}} |")
        print(f"| {'4. Exit':<{self.interface_size-2}} |")
        print("| " + " "*(self.interface_size-2) + " |")
        print("+" + "-"*self.interface_size + "+")

    def display_confirm_add(self, name, value, symbol):
        self.display_head_interface()
        print("| " + " "*(self.interface_size-2) + " |")
        print(f"| {f'Name: {name}':<{self.interface_size-2}} |")
        print(f"| {f'Value: {symbol}{value}':<{self.interface_size-2}} |")
        print("| " + " "*(self.interface_size-2) + " |")
        print("+" + "-"*self.interface_size + "+")
        print()

    # Flexible page interface
    def display_page_interface(self, page, actual_page, max_page, settings = False):
        # calc the page counter
        def get_page_counter(actual_page, max_page):
            def verify_positions(page_counter, max_page):
                # default values
                first_position = 0
                second_position = 0
                third_position = 0

                # if the page counter be more then 2 get the prev number of actual_page
                if len(page_counter) > 2:
                    first_position = f"{actual_page - 1} <- (prev)"
                else:
                    first_position = " "

                second_position = actual_page

                # if the page counter be more or equals to the max_page get the next number of actual_page
                if int(actual_page + 1) <= max_page:
                    third_position = f"(next) -> {actual_page + 1}"
                else:
                    third_position = " "

                return [first_position, second_position, third_position]

            page_counter = []

            # if actual page be different of 0 it gonna get a number less and a number more then the actual page to creates the counter
            if actual_page != 0:
                page_counter.extend(range(actual_page - 1, actual_page + 2))
            else:
                # but if the max page is 1 just creates 2 numbers in the page coutner (0, 1)
                if max_page > 1:
                    page_counter.extend(range(0, 2))
                else:
                    # and finally if is just a page, just get this page
                    page_counter.append(actual_page)

            # verify position to get the correct values for the interface
            page_counter = verify_positions(page_counter, max_page)
            return page_counter

        # gets the page counter
        page_counter = get_page_counter(actual_page, max_page)
        print("+" + "-"*self.interface_size + "+")
        print("| " + " "*(self.interface_size-2) + " |")
        print(f"| {'EXPENSE TRACKER':^{self.interface_size-2}} |")
        print("| " + " "*(self.interface_size-2) + " |")
        print("+" + "-"*self.interface_size + "+")
        print("| " + " "*(self.interface_size-2) + " |")

        # if extract_page is empty will print a empty message
        if page != "":
            # runs throught the extract page list
            for item in page:
                if not settings:
                    # get the currency symbol
                    symbol = get_currency_symbol(item[1]['currency'], item[1]['locale'])

                    print(f"| {f'{item[0]}. Name: {item[1]['name']} | Price: {symbol}{item[1]['value']}':<{self.interface_size-2}} |")
                else:
                    print(f"| {f'{page.index(item)}. {item[0]} ({get_currency_symbol(item[0], item[1])})':<{self.interface_size-2}} |")
        else:
            print(f"| {'EMPTY...':^{self.interface_size-2}} |")

        
        print("| " + " "*(self.interface_size-2) + " |")
        print("+" + "-"*self.interface_size + "+")
        print(f"| {f'{page_counter[0]}':<{(self.interface_size/3)}}{f'{page_counter[1]}':^{(self.interface_size/3)}}{f'{page_counter[2]}':>{(self.interface_size/3)}} |")
        
        if not settings:
            print(f"| {'(X) EXIT | (i) INFO | (E) EDIT | (T) TOTAL':^{self.interface_size-2}} |")
        else:
            print(f"| {'(X) EXIT | (S) SELECT':^{self.interface_size-2}} |")

        print("+" + "-"*self.interface_size + "+")

    def display_edit_or_confirm_expense(self, expense, month):
        symbol = get_currency_symbol(expense['currency'], expense['locale'])

        print("+" + "-"*self.interface_size + "+")
        print("| " + " "*(self.interface_size-2) + " |")
        print(f"| {'EXPENSE TRACKER':^{self.interface_size-2}} |")
        print(f"| {f'MONTH: {month}':^{self.interface_size-2}} |")
        print("| " + " "*(self.interface_size-2) + " |")
        print("+" + "-"*self.interface_size + "+")
        print("| " + " "*(self.interface_size-2) + " |")
        print(f"| {f'Name: {expense['name']}':<{self.interface_size-2}} |")
        print(f"| {f'Value: {symbol}{expense['value']}':<{self.interface_size-2}} |")
        print("| " + " "*(self.interface_size-2) + " |")
        print("+" + "-"*self.interface_size + "+")

    def display_expense_info(self, expense, symbol):
        self.display_head_interface()
        print("| " + " "*(self.interface_size-2) + " |")
        print(f"| {f'Name: {expense['name']}':<{self.interface_size-2}} |")
        print(f"| {f'Value: {symbol}{expense['value']}':<{self.interface_size-2}} |")
        print(f"| {f'Currency: {expense['currency']}':<{self.interface_size-2}} |")
        print(f"| {f'Registred Time: {expense['register_time']}':<{self.interface_size-2}} |")
        print("| " + " "*(self.interface_size-2) + " |")
        print("+" + "-"*self.interface_size + "+")
        print()
        input("...")

    def display_total_info(self, info, item_quantity):
            def get_total_and_media(info):
                # new lists to separete the info
                total = []
                media = []

                # gets the total and media to format with the currency symbol
                for item in info:
                    total.append(f"{get_currency_symbol(info[item]['currency'], info[item]['locale'])}{info[item]['expenses']:.2f}")
                    media.append(f"{get_currency_symbol(info[item]['currency'], info[item]['locale'])}{info[item]['expenses'] / info[item]['itens_quantity']:.2f}")

                # return both
                return total, media

            total, media = get_total_and_media(info)

            self.display_head_interface()
            print()
            print(f"  {f'Items quantity: {item_quantity}':<{self.interface_size-2}}  ")
            print(f"  {f'Media expended: {", ".join((item for item in media))}':<{self.interface_size-2}}  ")
            print(f"  {f'Total: {", ".join((item for item in total))}':<{self.interface_size-2}}  ")
            print()
            print("+" + "-"*self.interface_size + "+")
            print()
            input("...")

    def display_settings(self, config):
        self.display_head_interface()
        print("| " + " "*(self.interface_size-2) + " |")
        print(f"| {f'1. Change Currency ({config.currency})':<{self.interface_size-2}} |")
        print(f"| {f'2. Load a different file ({config.default_month})':<{self.interface_size-2}} |")
        print(f"| {'3. Exit':<{self.interface_size-2}} |")
        print("| " + " "*(self.interface_size-2) + " |")
        print("+" + "-"*self.interface_size + "+")

    # Flexible invalid message
    def display_invalid_message(self, text="Please, insert a valid option"):
        print("+" + "-"*self.interface_size + "+")
        print("| " + " "*(self.interface_size-2) + " |")
        print(f"| {f'{text}':<{self.interface_size-2}} |")
        print("| " + " "*(self.interface_size-2) + " |")
        print("+" + "-"*self.interface_size + "+")
        print()
        input("...")