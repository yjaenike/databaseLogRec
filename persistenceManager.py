import os


class PersistenceManager:
    _instance = None

    test = 5

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(PersistenceManager, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def begin_transaction(self) -> int:
        """
        :return: transaction id
        """
        return 0

    def commit(self, ta_id: int) -> bool:
        """
        :param ta_id: transaction id
        :return: true if successful
        """
        pass

    def write(self, ta_id: int, page_id: int, data: str):
        """
        :param ta_id: transaction id
        :param page_id: page id
        :param data: user data
        :return: None
        """
        pass

    def write_data_to_file(self, lsn, pageid, data):
        try:
            f = open('pages/page_{}.txt'.format(pageid), "w")
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
    pm.test = 6;
    pm2 = PersistenceManager()
    print(pm2.test)


if __name__ == "__main__":
    main()
