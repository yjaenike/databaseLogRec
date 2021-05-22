import random
from time import sleep

class Client():

    def __init__(self, id):
        # transactions is a nested list:
        self.transactions = []
        self.id = id

    # def checkTransactions(self):
    #     t = [item for sublist in self.transactions for item in sublist]
    #     t = [o.split(":")[0] for o in t]
        
    #     if t[0] != 'b':
    #         return false

    def begin(self):
        self.transactions.append(["b"])

    def write(self, data):
        self.transactions[-1].append("w:{}".format(data))

    def commit(self):
        self.transactions[-1].append("c")

    def __str__(self):
        #Do whatever you want here  
        return str(self.transactions)

    def execute_transactions(self):

        for transaction in self.transactions:
            for operation in transaction:
                sec = round(random.random(),2)
                sleep(sec)
                print(operation)
                yield operation


def main():
    c = Client(1)

    c.begin()
    c.write("1")
    c.write("2")
    c.write("3")
    c.commit()
    
    c.begin()
    c.write("1a")
    c.write("2b")
    c.write("3c")
    c.commit()

    for o in c.execute_transactions():
        pass

if __name__ == "__main__":
    main()
