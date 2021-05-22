from client import Client
from persistenceManager import PersistenceManager
from multiprocessing import Process

def main():
    # create a persistence manager
    pm = PersistenceManager()
    print("Created Persistence Manager...")

    # generate a pool of clients with transactions to execute
    clients = createClients()
    print("Generated Clients...")

    # create a Thread Pool to execute clients synchronosly
    for c in clients:
        c.start()


def createClients():
    '''
    This function is used to create the different clients and give them back in a list 
    '''
    c1 = Client(1)
    c1.begin()
    c1.write(1, "Hans Peter")
    c1.write(2, "Berta Klausen")
    c1.write(2, "Celine Mainke")
    c1.commit()

    c2 = Client(2)
    c2.begin()
    c2.write(1, "Alex Bayer")
    c2.write(2, "Mads Höfer")
    c2.write(2, "Cornelia Hansen")
    c2.commit()

    c3 = Client(3)
    c3.begin()
    c3.write(1, "Wiebke Tomsen")
    c3.write(2, "Rieke Mayer")
    c3.write(2, "Kim Tran")
    c3.commit()

    clients = [c1,c2,c3]

    return clients



if __name__ == "__main__":
    main()