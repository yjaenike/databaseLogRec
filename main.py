from client import Client
from persistenceManager import PersistenceManager
from multiprocessing import Process

def main():
    # create a persistence manager
    pm = PersistenceManager()
    print("Created Persistence Manager...\n")

    # generate a pool of clients with transactions to execute
    clients = createClients(pm)
    print("Generated Clients...\n")

    print("################## Clients ##################")
    for c in clients:
        print(c)
    print("############################################\n")

    # create a Thread Pool to execute clients synchronosly
    for c in clients:
        c.start()

    for c in clients:
        c.join()
    print("All clients finished...\n")

    # TODO: what happens next? o.O

def createClients(pm):
    '''
    This function is used to create the different clients and give them back in a list 
    '''
    c1 = Client(1,pm)
    c1.begin()
    c1.write(1, "Hans Peter")
    c1.write(2, "Berta Klausen")
    c1.write(3, "Celine Mainke")
    c1.write(4, "Klaus Müller")
    c1.write(5, "Peter parker")
    c1.write(6, "Tony Stark")
    c1.commit()

    c1.begin()
    c1.write(7, "Klaus Müller")
    c1.write(8, "Peter parker")
    c1.write(9, "Tony Stark")
    c1.commit()

    c2 = Client(2,pm)
    c2.begin()
    c2.write(1, "Alex Bayer")
    c2.write(2, "Mads Höfer")
    c2.write(2, "Cornelia Hansen")
    c2.commit()

    c3 = Client(3,pm)
    c3.begin()
    c3.write(1, "Wiebke Tomsen")
    c3.write(2, "Rieke Mayer")
    c3.write(2, "Kim Berly")
    c3.commit()

    clients = [c1,c2,c3]

    return clients



if __name__ == "__main__":
    main()