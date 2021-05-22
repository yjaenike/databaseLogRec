import os

class PersistenceManager():

    #def __init__(self):

    def write_data_to_file(self, lsn, pageid, data):
        try:
            f = open('pages/page_{}.txt'.format(pageid),"w")
            f.write(data)
            f.close()
        except FileNotFoundError:
            print('File does not exist')

    def write_log_to_file(self, lsn, taid, pageid, data):
        try:
            f = open('filename')
            # do stuff with log here
            f.close()
        except FileNotFoundError:
            print('File does not exist')        

def main():
    pm = PersistenceManager()

if __name__ == "__main__":
    main()
