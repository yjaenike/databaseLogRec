import random
from time import sleep
from threading import Thread


class WrongPageIdException(Exception):
    pass

class UnknownOperationException(Exception):
    pass

class Client(Thread):

    def __init__(self, id, pm):
        '''ransactions is a nested list. Each transaction consists of multipl operations. The beginn operation is marked as a b, teh commit operation as a c and the write operation as a w. The w is followed by the pageid and by the user data seperated by a colon. '''
        super().__init__()
        self.transactions = []
        self.id = id
        self.pm = pm

    def begin(self):
        '''adds a new sublist (transactionlist) to the transactions list and inserts a b into that list for begin of transaction'''
        self.transactions.append(["b"])

    def write(self,page: int, data: str):
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

        return r

    def execute(self):
        ''' Used to yield back the operations of the different transactions  '''
        for transaction in self.transactions:
            ta_id = -1
            for operation in transaction:
                sec = round(random.random(),2)
                sleep(sec)
                #print("client-{}: {}".format(self.id,operation))
                
                # check type of operation and execute on pm
                if operation[0] == "b":
                    # generate transaction number
                    ta_id = self.pm.begin_transaction()
                
                elif operation[0] == "w":
                    # extract information from the operation
                    operation_data = operation.split(":")
                    page_id = operation_data[1]
                    data = operation_data[2]

                    # execute the write function of the persistence manager using the collected data
                    self.pm.write(ta_id, page_id, data)
                    print("clinet-{} - ta_id: {}, page id: {}, data: {}".format(self.id, ta_id, page_id, data))

                elif operation[0] == "c":
                    # commit the transaction
                    self.pm.commit(ta_id)

                else:
                    raise UnknownOperationException("Something went wrong with the creation if the transactions!")



    def run(self):
        self.execute()
