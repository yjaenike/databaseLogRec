import os

class PersistenceManager():

    #def __init__(self):

    def write_to_file(self, lsn, pageid, data):
        try:
            f = open('pages/page_{}.txt'.format(pageid),"w")
            f.write(data)
            f.close()
        except FileNotFoundError:
            print('File does not exist')

        

def main():
    pm = PersistenceManager()

    pm.write_to_file(2,2,"hello earth")

if __name__ == "__main__":
    main()
