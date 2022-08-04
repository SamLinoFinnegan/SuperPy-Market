import csv
import os
from datetime import datetime, date, timedelta
from gooey import Gooey, GooeyParser
from rich.table import Table
from rich.console import Console
from openpyxl import Workbook
import string

alphabet = string.ascii_uppercase

workbook = Workbook()
sheet = workbook.active


PATH_TXT =os.path.join(os.getcwd(), os.path.basename('time.txt'))
time_file_exists = os.path.isfile(PATH_TXT)  

def create_time_file(time):
    if time == "reset":
        os.remove(PATH_TXT)
    elif time in "1234567890":
        with open(PATH_TXT, "w") as write_file:
            write_file.write(time)
    else:
        print("That is an invalid input, use 1234567890 or the word reset")
        
if time_file_exists:
    with open("C:/Users/samue/Projects/Back-end/SuperPy_market/time.txt", "r") as read_file:
        num = read_file.read()
        now = date.today() + timedelta(days=int(int(num)))
else:
    now = date.today()
yesterday = now - timedelta(days=1)
tomorrow = now + timedelta(days=1)

@Gooey(
    program_name='My Supermarkt APP',
    show_preview_warning=False,
    advanced=True,
    navigation='TABBED',
    header_bg_color="#f69c00",

    menu=[{'name': 'Help', 'items': [{'type': 'AboutDialog',
                                      'menuTitle': 'About',
                                      'name': 'My Supermarket APP',
                                      'description': 'This is a little summary on how to use this app, you have three main options: 1 Buy is where you can purchase items to add to your store, 2 Sell is where you can sell the same items to your costumers, 3 Reports is where you can get your reports on how your store is going',
                                      'version': '1.2.1',
                                      'copyright': '2022', }]}]
)
def parser_function():
    parser = GooeyParser(
        description="Welcome to the My Supermarket, the tool to help you run your store")
    subparser = parser.add_subparsers(
        dest='command', description="Choose from the diferent departments [Buy , Sell , Stock , Search_Report]")

    buy_parser = subparser.add_parser('Buy')
    sell_parser = subparser.add_parser('Sell')
    stock_parser = subparser.add_parser("Stock")
    search_parser = subparser.add_parser("Search_Report")
    advance_time_parser = subparser.add_parser("Advance_time")


    #############################################################################
    buy_parser.add_argument('-p', '--Product', required=True, type=str,
                            help="Product that you would like to ADD to your store")


    buy_parser.add_argument('-q', '--Quantity', required=True, type=int,
                            help="How many would you like add?")

    buy_parser.add_argument('-b', '--Bought', required=True, type=float,
                            help="The price you BOUGHT the product for")
    buy_parser.add_argument(
        '-e', '--Expiration',  required=True, help="Expiration date on the Product e. g (yyyy-mm-dd)", widget="DateChooser")

    ##############################################################################
    sell_parser.add_argument('-p', '--Product',  required=True, type=str,
                                help="Which product that you have in your store that you wish to SEll")
    sell_parser.add_argument('-q', '--Quantity', required=True, type=int,
                            help="How many would you like sell?")
    sell_parser.add_argument(
        '-s', '--Sell', required=True, type=float, help="Price you wish to SELL the product for")


    #############################################################################
    stock_group = stock_parser.add_argument_group(
        "Stock", "Check the products you currently have in your store")
    stock_group.add_argument(
        '-p', '--print', action="store_true", default=False)


    #########################################################################
    search_group = search_parser.add_argument_group(
        "Search_Report", "Search though inventory history ")

    search_group.add_argument('-from', '--Start',
                                help="Type in the dates you would like to see your inventory report (supported formats .e .g yyyy-mm-dd, now, yesterday, 3days, 5weeks 2months) ", widget="DateChooser")
    search_group.add_argument('-till', '--End',
                                help="Type in the dates you would like to see your inventory report (supported formats .e .g yyyy-mm-dd, now, yesterday, 3days, 5weeks 2months)", widget="DateChooser")
    search_group.add_argument('Department', choices=(
        "Inventory", "Revenue", "Profit", "Waste"), help="You have to pick wich report you would like to see")
    search_group.add_argument('-export', '--Export', action="store_true",  help="If you would like to export your report to an EXCEL sheet")
    #########################################################################
    advance_time_parser.add_argument('-a', '--Advance', help="You can change the current date, use this flag, to simulate action in the future, use the number of days in the future that you would like to change the current date in the program, or use the, reset, keyword to reset to original time ")
    
    args = parser.parse_args()
    return args


CSV_PATH = os.path.join(os.getcwd(), os.path.basename('bought.csv'))
bought_file_exists = os.path.isfile(CSV_PATH)

CSV_SELL_PATH = os.path.join(os.getcwd(), os.path.basename("sold.csv"))
sell_file_exists = os.path.isfile(CSV_SELL_PATH)

class SuperPy:

    sold_field_names = ["ID", "Product","Quantity","Sold_price", "Sold_date",
                        "Expiration"]
    bought_field_names = ["ID", "Product","Quantity" , "Bought_price", "Bought_date",
                            "Expiration", "InStock"]

    def incre(count):
        count += 1
        return count

    def open_read_bought():
        with open('bought.csv', 'r', newline="") as output:
            csv_reader = csv.DictReader(output)
            copy_bought_reader = [line for line in csv_reader]

            return copy_bought_reader

    def open_read_sold():
        with open('sold.csv', 'r', newline="") as sold_read:
            csv_sell_reader = csv.DictReader(sold_read)
            copy_sold_reader = [line for line in csv_sell_reader]
            return copy_sold_reader

    def check_lowest_ex(product, reader):
        day_list = list()

        expiration_list = [line["Expiration"]
                            for line in reader if product == line["Product"] and line['InStock'] == "True"]
        
        if len(expiration_list) == 0:
            return print(f"Sorry! but you dont have anymore: {product}s in your inventory")

        for date in expiration_list:  # function to determine lowest expiration date

            ExpirationDate = datetime.strptime(
                date, "%Y-%m-%d").date()
            amount_days = ExpirationDate - now

            if int(amount_days.days) > 0:
                day_list.append(int(amount_days.days))
            lowest = min(day_list)

        return lowest

    def check_time(time):
        if time == "now":
            the_date = now
        elif time == "yesterday":
            the_date = yesterday
        elif time[0] in "1234567890" and time[-1:] in "wekdaymonths":
            time_arr = list(time)
            num = int(time_arr.pop(0))
            str_time = "".join(time_arr)
            if str_time == "weeks" or str_time == "week":
                the_date = now - timedelta(days=7 * num)
            elif str_time == "month" or str_time == "months":
                the_date = now - timedelta(days=30 * num)
            elif str_time == "day" or str_time == "days":
                the_date = now - timedelta(days=1 * num)
        elif time[:2] == "20":

            the_date = datetime.strptime(
                time, "%Y-%m-%d").date()

        return the_date

    def add_value(start, end, reader, r):
        total = 0
        start_date = datetime.strptime(
            start, "%Y-%m-%d").date()
        if r == "sold":
            var_date = "Sold_date"
            var_value = "Sold_price"
        else:
            var_date = "Bought_date"
            var_value = "Bought_price"
        for line in reader:
            current_date = datetime.strptime(
                line[var_date], "%Y-%m-%d").date()
            if end:
                end_date = datetime.strptime(
                    end, "%Y-%m-%d").date()
                if start_date <= current_date and end_date >= current_date:
                    rev = float(line[var_value]) * int(line['Quantity'])
                    total += float(rev)
            else:
                the_date = start_date
                if the_date == current_date:
                    rev = float(line[var_value]) * int(line['Quantity'])
                    total += float(rev)
        return total

    def check_expired_products(reader):
        for line in reader:
            expiration_date = datetime.strptime(
                line["Expiration"], "%Y-%m-%d").date()

            if expiration_date < now:
                line["InStock"] = "Expired"

        writer = csv.DictWriter(
            open('bought.csv', 'w', newline=''), fieldnames=SuperPy.bought_field_names)
        writer.writeheader()
        for line in reader:
            writer.writerow(line)

    def print_stock_or_waste(variable):

        new_header_str =[]
        for item in SuperPy.bought_field_names:
            new_header_str.append("{:>8}".format(item)) 
        print("===================================")
        print(new_header_str)
        print("===================================")
        copy_bought_reader = SuperPy.open_read_bought()
        for line in copy_bought_reader:
            if line["InStock"] == variable:

                print(
                    "{:<8} {:<10} {:<10} {:<10} {:>10} {:>15} {:>10}".format(line["ID"],line["Product"],line["Quantity"],line["Bought_price"],line["Bought_date"],line["Expiration"],line["InStock"]))

        print("===================================")

    def check_same_product(product, quant,bought, expiration,key, price, reader):
        
        boolean_list =[]
        
        for line in reader:# the csv in memory
            # my variables in the line
            
            i, p, q, b, ex =line["ID"], line["Product"], line["Quantity"], line[price], line["Expiration"]
            # Check if the exact same item is in my file, and if so add them together
            
            last_id = i
            
            if (p == product and float(b) == bought and ex == expiration):
                
                new_quant = int(q) + quant
                line["Quantity"] = new_quant # update line quantity
                boolean_list.append(False)
            else:
                boolean_list.append(True)

            if key == "bought":        # creating the trigger to write if product is not the ame product
                SuperPy.bought_writer(reader) #update csv file with new value    
            elif key == "sold":
                SuperPy.sold_writer(reader)
        if all(boolean_list): # if product is not in csv file
            my_r = [True, int(last_id)]
        else:
            my_r = [False, int(last_id)]
        return my_r 
      
    def bought_writer(reader):
        writer = csv.DictWriter(
        open('bought.csv', 'w', newline=''), fieldnames=SuperPy.bought_field_names) #update bought file
        writer.writeheader()
        for line in reader:
            writer.writerow(line) 
    
    def sold_writer(reader):
        writer = csv.DictWriter(
        open('sold.csv', 'w', newline=''), fieldnames=SuperPy.sold_field_names) #update bought file
        writer.writeheader()
        for line in reader:
            writer.writerow(line) 
# ####################################################################################################################################

class Buy(SuperPy):
    def __init__(self, product, quantity,  bought, expiration):
        lower_product = product.lower()
        self.product = lower_product
        self.quantity = quantity
        self.bought = bought
        self.expiration = expiration

    def add_inventory(self):
        try:

            with open('bought.csv', 'a', newline="") as add_input:
                csv_writer = csv.DictWriter(
                    add_input, fieldnames=SuperPy.bought_field_names)
                
                csv_reader = SuperPy.open_read_bought()
                if not bought_file_exists:
                    id = 1
                    csv_writer.writeheader()
                    csv_writer.writerow(
                        {"ID": id, 'Product': self.product, 'Quantity':self.quantity, 'Bought_price': self.bought, "Bought_date": now, 'Expiration': self.expiration, 'InStock': True})
                
                elif bought_file_exists:
                    key = "bought"
                    price = 'Bought_price'
                    result = SuperPy.check_same_product(self.product, self.quantity, self.bought, self.expiration, key,price, csv_reader)
                    
                    if result[0]:
                        
                        id = result[1]
                        csv_writer.writerow(
                        {"ID": SuperPy.incre(id), 'Product': self.product, 'Quantity':self.quantity, 'Bought_price': self.bought, "Bought_date": now, 'Expiration': self.expiration, 'InStock': True})


                    
        except Exception as e:
            print(e)
################################################################################################################################

class Sell(SuperPy):
    def __init__(self, product, quantity, sold):
        lower_product = product.lower()
        self.product = lower_product
        self.quantity = quantity
        self.sold = sold

    def sell_products(self):
        try:
            with open('sold.csv', 'a', newline="") as sold_input:
                csv_sell_writer = csv.DictWriter(
                    sold_input, fieldnames=SuperPy.sold_field_names)


                copy_bought_reader = SuperPy.open_read_bought()
                lowest = SuperPy.check_lowest_ex( #closest to expire
                        self.product, copy_bought_reader)

                if sell_file_exists:
                    csv_sell_reader = SuperPy.open_read_sold()
                    for line in csv_sell_reader:     # to get the ID number
                        c = line["ID"]
                        id = int(c)
                else:
                    id = 1
                if bought_file_exists:      # check bought file exists
                    
                    condition = True
                    for line in copy_bought_reader:

                        expiration = line.get("Expiration") # find out how many day miising till expiration of product on current line
                        current_ex = datetime.strptime(
                            expiration, "%Y-%m-%d").date()
                        current_num = current_ex - now
                        
                        if int(current_num.days) > 0:  # check if the item is expired
                            correct_num = int(current_num.days)
                        else:
                            line["InStock"] = "Expired"

                        quant = int(self.quantity)

                        while condition:  # function that will count down quantity till 0
                            copy_bought_reader = SuperPy.open_read_bought()
                            for inner_line in copy_bought_reader:
                                
                                low = SuperPy.check_lowest_ex(
                                self.product, copy_bought_reader)

                                line_quant = int(inner_line["Quantity"])
                                
                                expiration = inner_line.get("Expiration")
                                current_ex = datetime.strptime(
                                    expiration, "%Y-%m-%d").date()
                                inner_current_num = current_ex - now
                                
                                
                                if int(current_num.days) > 0:  # check if the item is expired
                                    inner_current_num = int(current_num.days)
                                else:
                                    inner_line["InStock"] = "Expired"

                                SuperPy.bought_writer(copy_bought_reader)

                                if low == inner_current_num and self.product == inner_line['Product'] and inner_line["InStock"] == "True":
                                    
                                    if condition:

                                        if quant > line_quant:
                                            quant = quant - line_quant
                                            inner_line["Quantity"] = line_quant - line_quant

                                        else:
                                            x = quant
                                            quant = quant - quant
                                            inner_line['Quantity'] = line_quant - x

                                    if inner_line["Quantity"] == 0:
                                        inner_line["InStock"] = False
                
                                    if quant == 0:
                                        condition = False


                                    SuperPy.bought_writer(copy_bought_reader)   
                                  
                        if lowest == correct_num and self.product == line['Product']: #grab the product with the closest expiration date
                            
                            if not sell_file_exists:  # if sold file is not created yet
                                id = 1
                                if line["Quantity"] == 0:
                                    line["InStock"] = False
                                csv_sell_writer.writeheader()
                                csv_sell_writer.writerow(
                                    {"ID": id, 'Product': self.product, 'Quantity':self.quantity,
                                        'Sold_price': self.sold, "Sold_date": now, 'Expiration': expiration}
                                )
                                print("Item sold")
                                break # just to make sure it only runs once
                            if sell_file_exists:
                                sold_csv_reader = SuperPy.open_read_sold()
                                key = "sold"
                                price = 'Sold_price'
                                sell_result = SuperPy.check_same_product(self.product, self.quantity, self.sold, expiration, key,price, sold_csv_reader)
                                if sell_result[0]:

                                    id = sell_result[1]

                                    if line["Quantity"] == 0:
                                        line["InStock"] = False

                                    csv_sell_writer.writerow(
                                        {"ID": SuperPy.incre(id), 'Product': self.product, 'Quantity':self.quantity,
                                            'Sold_price': self.sold, "Sold_date": now, 'Expiration': expiration}
                                    )
                                    print("Item sold")
                                    break

                else:
                    print(
                        "ID  Item  Bought_price  Bought_date  Expiration  InStock")
                    print("Your inventory is empty")

            SuperPy.bought_writer(copy_bought_reader)
            

        except Exception as e:
            print(e)


#################################################################################################################

class Report(SuperPy):
    def __init__(self, sector, sta_dat, end_dat, ex):
        self.sector = sector
        self.sta_dat = sta_dat
        self.end_dat = end_dat
        self.ex = ex

    def records(self):
        

        try:
            copy_bought_reader = SuperPy.open_read_bought()
            copy_sold_reader = SuperPy.open_read_sold()

            SuperPy.check_expired_products(copy_bought_reader)

            
            
            time_str = "{} {}".format(self.sta_dat," till " + self.end_dat if self.end_dat is not None else"")
            key_list = []
            if self.sector == "Inventory":
                table = Table(title="Inventory")
                for line in copy_bought_reader:
                    key_list.extend(line.keys())
                    for key , letter in zip(key_list, alphabet[:len(key_list)]):
                        table.add_column(key)
                        sheet[letter + "1"] = key
                    break
                
                row = 2
                for line in copy_bought_reader:
                    current_date = datetime.strptime(
                        line["Bought_date"], "%Y-%m-%d").date()

                    if self.end_dat == None:
                        the_date = SuperPy.check_time(self.sta_dat)
                        if the_date == current_date:
                            table.add_row("%s"%line["ID"],"%s"%line["Product"],"%s"%line["Quantity"],"%s"%line["Bought_price"],"%s"%line["Bought_date"],"%s"%line["Expiration"],"%s"%line["InStock"])
                            
                            for key ,letter in zip(key_list , alphabet[:len(key_list)]): # write eache row to the excell file

                                sheet[letter + str(row)] = line[key]
                        row +=1        

                    if self.end_dat is not None:

                        stadate = self.sta_dat
                        endate = self.end_dat

                        start_date = datetime.strptime(
                            stadate, "%Y-%m-%d").date()

                        end_date = datetime.strptime(
                            endate, "%Y-%m-%d").date()

                        if start_date <= current_date and end_date >= current_date:
                            table.add_row("%s"%line["ID"],"%s"%line["Product"],"%s"%line["Quantity"],"%s"%line["Bought_price"],"%s"%line["Bought_date"],"%s"%line["Expiration"],"%s"%line["InStock"])

                            for key ,letter in zip(key_list , alphabet[:len(key_list)]): # write eache row to the excell file

                                sheet[letter + str(row)] = line[key]
                        row +=1
                
                
                console = Console()
                console.print(table)        
                if self.ex:
                    workbook.save(filename="inventory_rep.xlsx")
            
            elif self.sector == "Revenue":# have to see how to get the last cell in excel
                table = Table(title="Revenue")

                for line in copy_sold_reader:
                    key_list.extend(line.keys())
                    for key , letter in zip(key_list, alphabet[:len(key_list)]):
                        table.add_column(key)
                        sheet[letter + "1"] = key
                    break
                
                row = 2
                total_rev = SuperPy.add_value(
                    self.sta_dat, self.end_dat, copy_sold_reader, "sold")
                for line in copy_sold_reader:
                    for key ,letter in zip(key_list , alphabet[:len(key_list)]): # write eache row to the excell file

                        sheet[letter + str(row)] = line[key]
                    row +=1
                
                
                
                rev_str ="Your Revenue from "+time_str +f" was {total_rev}"
                print(rev_str)
                
                
                sheet["A" + str(row +1)] = rev_str
                
                
                if self.ex:
                    workbook.save(filename="Revenue_rep.xlsx")

            elif self.sector == "Profit":
                total_rev = SuperPy.add_value(
                    self.sta_dat, self.end_dat, copy_sold_reader, "sold")
                total_spent = SuperPy.add_value(
                    self.sta_dat, self.end_dat, copy_bought_reader, "bought")
                profit = total_rev - total_spent

                print("Your Profit from "+time_str +f" was {profit}")
                
        except FileNotFoundError:
            print("You havent created your inventory file or your sold file yet")
            print("Your inventory is empty")


#################################################################################################################
def main():
    args = parser_function()

    if args.command == "Buy":
        Store = Buy(args.Product, args.Quantity, args.Bought, args.Expiration)
        Store.add_inventory()
        print(f"OK, {args.Quantity} {args.Product} added to your inventory")
    elif args.command == "Sell":
        Store = Sell(args.Product,args.Quantity, args.Sell)
        Store.sell_products()

    elif args.command == "Stock":
        if args.print:
            SuperPy.print_stock_or_waste("True")
    elif args.command == "Search_Report":
        if args.Department == "Waste":
            SuperPy.print_stock_or_waste("Expired")

        else:
            Store = Report(args.Department, args.Start, args.End, args.Export)
            Store.records()
    elif args.command == "Advance_time":
        create_time_file(args.Advance)
        
       

if __name__ == '__main__':
    main()
