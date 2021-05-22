from typing import Dict, List


class Page:
    lsn: int
    user_data: str
    dirty: bool

    def __init__(self, lsn: int, user_data: str):
        self.write(lsn, user_data)

    def write(self, lsn: int, user_data: str):
        self.lsn = lsn
        self.user_data = user_data
        self.dirty = True

    def commit(self, lsn: int):
        self.lsn = lsn
        self.dirty = False

    # TODO: kann weg?
    @classmethod
    def from_page_file(cls, file: str):
        """
        Constructor to create page buffer entry from stored file
        :param file: string from page file containing
        :return: new page object
        """
        lsn = int(file.split(',')[0])
        user_data = file.split(',')[1]
        return cls(lsn, user_data)


class PersistenceManager:
    _instance = None
    buffer: Dict[int, Page] = {}
    next_transaction_id: int = 0
    next_lsn: int = 0

    running_transactions: Dict[int, List[int]]

    def __new__(cls):
        # singleton
        if cls._instance is None:
            cls._instance = super(PersistenceManager, cls).__new__(cls)
        return cls._instance

    def begin_transaction(self) -> int:
        """
        :return: transaction id
        """
        self.next_transaction_id += 1
        return self.next_transaction_id

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
        # write to log
        self.__write_log_entry_data(self.next_lsn, ta_id, page_id, data)

        # write to buffer (to-do: persistence handling)
        if page_id not in self.buffer:
            self.buffer[page_id] = Page(self.next_lsn, data)
        else:
            self.buffer[page_id].write(self.next_lsn, data)

        self.next_lsn += 1

    @staticmethod
    def __write_data_to_file(lsn, page_id, data):
        try:
            f = open('pages/page_{}.txt'.format(page_id), "w")
            f.write(data)
            f.close()
        except FileNotFoundError:
            print('File does not exist')

    @staticmethod
    def __write_log_entry_data(lsn: int, ta_id: int, page_id: int, user_data: str):
        try:
            f = open('log.txt', 'a')
            log_entry = f"{lsn},{ta_id},{page_id},{user_data}\n"
            f.write(log_entry)
            f.close()
        except FileNotFoundError:
            print('File does not exist')


def main():
    pm = PersistenceManager()
    ta_id = pm.begin_transaction()
    pm.write(ta_id, 3, "test bla")
    pm.commit(ta_id)

    ta_id = pm.begin_transaction()
    pm.write(ta_id, 4, "test bla2")
    pm.commit(ta_id)


if __name__ == "__main__":
    main()
