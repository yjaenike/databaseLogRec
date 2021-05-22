class Client():

    def __init__(self):
        # transactions is a nested list:
        self.transactions = []

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

    def execute_transactions:
        

def main():
    c = Client()

    c.begin()
    c.write("1")
    c.write("2")
    c.write("3")
    c.commit()
    
    c.write("1a")
    c.write("2b")
    c.write("3c")
    c.commit()

    c.checkTransactions()

if __name__ == "__main__":
    main()
