# class methods


class Account:

    def __init__(self, owner, money):
        self.owner = owner
        self.money = money

    def add_money(self, amount):
        self.money += amount
        print("New balance:", self.money)


acc = Account("Cook", 100)
acc.add_money(50)