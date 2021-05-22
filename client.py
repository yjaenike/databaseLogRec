import random
from time import sleep
from threading import *


class WrongPageIdException(Exception):
    pass


class Client(Thread):

    def __init__(self, id, buffer):
        # transactions is a nested list. Each transaction consists of multipl operations. The beginn operation is marked as a b, teh commit operation as a c and the write operation as a w. The w is followed by the pageid and by the user data seperated by a colon. 
        super().__init__()
        self.transactions = []
        self.id = id
        self.buffer = buffer

    def begin(self):
        '''adds a new sublist (transactionlist) to the transactions list and inserts a b into that list for begin of transaction'''
        self.transactions.append(["b"])

    def write(self,page, data):
        ''' writes a write entry to the latest transaction including the pageid it will be written to and the data it wants to write seperated by colons'''

        if page not in [i for i in range(0,10)]:
            raise WrongPageIdException("The page needs to be between 0 & 10")

        self.transactions[-1].append("w:{}{}:{}".format(self.id,page,data))

    def commit(self):
        ''' adds a c to the last transaction to signal a commit, endling of that transaction.'''
        self.transactions[-1].append("c")

    def __str__(self):

        r = "Client id={}\n".format(self.id)
        r = r + " # of trans: " + str(len(self.transactions))+"\n"
        for i, t in enumerate(self.transactions):
            r = r + " Trans. {}: {} \n".format(i, t)

        return r+"\n"

    def execute(self):
        ''' Used to yield back the operations of the different transactions  '''
        for transaction in self.transactions:
            for operation in transaction:
                sec = round(random.random(),2)
                sleep(sec)
                print("client-{}: {}".format(self.id,operation))
                #yield operation
    
    def run(self):
        self.execute()


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

    print(c)

    for o in c.execute():
        pass

if __name__ == "__main__":
    main()
