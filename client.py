import random
from time import sleep

class Client():

    def __init__(self, id):
        # transactions is a nested list. Each transaction consists of multipl operations. The beginn operation is marked as a b, teh commit operation as a c and the write operation as a w. The w is followed by the pageid and by the user data seperated by a colon. 
        self.transactions = []
        self.id = id

    def begin(self):
        self.transactions.append(["b"])

    def write(self,page, data):
        self.transactions[-1].append("w:{}:{}".format(page,data))

    def commit(self):
        self.transactions[-1].append("c")

    def __str__(self):
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
    c.write(1, "a")
    c.write(2, "b")
    c.write(2, "c")
    c.commit()
    
    c.begin()
    c.write(1, "f")
    c.write(2, "x")
    c.write(3, "z")
    c.commit()

    for o in c.execute_transactions():
        pass

if __name__ == "__main__":
    main()
