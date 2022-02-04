class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        print(self.name.center(30, '*'))
        for i in self.ledger:
            print('{1:23.23s}{0:>7.2f}'.format(i['amount'], i['description']))
        return 'Total: {}'.format(self.get_balance())

    def deposit(self, amount, description=""):

        globals()[f"{self.name}"] = {}
        globals()[f"{self.name}"]['amount'] = float(amount)
        globals()[f"{self.name}"]['description'] = description
        self.ledger.append(globals()[f"{self.name}"])

    def withdraw(self, amount, description=''):
        amount = float(amount)
        if self.check_funds(amount):
            globals()[f"{self.name}"] = {}
            globals()[f"{self.name}"]['amount'] = -amount
            globals()[f"{self.name}"]['description'] = description
            self.ledger.append(globals()[f"{self.name}"])
            return True
        else:
            return False

    def get_balance(self):
        amounts = []
        for i in self.ledger:
            amounts.append(i['amount'])
        return sum(amounts)

    def transfer(self, amount, name2):
        amount = float(amount)
        if self.check_funds(amount):
            withdraw_description = 'Transfer to {}'.format(name2.name)
            deposit_description = 'Transfer from {}'.format(self.name)
            self.withdraw(amount, withdraw_description)
            name2.deposit(amount, deposit_description)
            return True
        else:
            return False

    def check_funds(self, amount):
        ledger_amount = self.get_balance()
        if float(amount) > ledger_amount:
            return False
        else:
            return True


def create_spend_chart(categories):
    category_dict = {}
    sum_list = []

    for i in categories:
        globals()[f'i'] = []
        for e in i.ledger:
            if e['amount'] < 0:
                globals()[f'i'].append(e['amount'])

        category_dict[i.name] = sum(globals()[f'i'])
        sum_list.append(sum(globals()[f'i']))
    total = sum(sum_list)
    percentage_dict = {}

    chart_str = 'Percentage spent by category\n'
    for i in reversed(range(11)):
        chart_str += '{:>2}|'.format(str(i*10))
        for k, v in category_dict.items():
            percentage = (v / total) * 100
            percentage = round(percentage / 10)
            percentage_dict[k] = percentage
            if i < percentage:
                chart_str += '   o'
            else:
                chart_str += ''
        chart_str += '\n'
    chart_str += '   --'
    for n in range(len(sum_list)):
        chart_str += '----'
    chart_str += '\n'

    for i in range(max([len(k) for k, v in category_dict.items()])):
        chart_str += '    '
        for k, v in category_dict.items():
            if len(k) > i:
                chart_str += '   '
                chart_str += k[i]
            else:
                chart_str += '    '
        chart_str += '\n'

    return chart_str.rstrip() + ' '

food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

print(food)
print(clothing)

print(create_spend_chart([food, clothing, auto]))
