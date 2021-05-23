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
    buffer_size = 5
    next_transaction_id: int = 0
    next_lsn: int = 0

    running_transactions: Dict[int, List[int]] = {}

    def __new__(cls):
        # singleton
        if cls._instance is None:
            cls._instance = super(PersistenceManager, cls).__new__(cls)
            cls.__clear_log_entry()
        return cls._instance

    def begin_transaction(self) -> int:
        """
        :return: transaction id
        """
        self.next_transaction_id += 1

        self.running_transactions[self.next_transaction_id] = []
        return self.next_transaction_id

    def commit(self, ta_id: int) -> bool:
        """
        :param ta_id: transaction id
        :return: true if successful
        """

        # commit pages and clean from running_transactions
        for page_id in self.running_transactions[ta_id]:
            self.buffer[page_id].commit(self.next_lsn)
        self.running_transactions.pop(ta_id)

        # write log
        self.__write_log_entry_eot(self.next_lsn, ta_id)

        # increment lsn
        self.next_lsn += 1

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

        # remember affected pages for this transaction
        self.running_transactions[ta_id].append(page_id)

        # increment lsn
        self.next_lsn += 1

        if self.check_buffer():
            self.clear_buffer()

    def check_buffer(self):
        ''' returns True if the buffer size is bigger then allowed buffer size, else False'''
        return len(self.buffer) > self.buffer_size
    
    def clear_buffer(self):
        '''
        Runners over the list of running transactions to collect all pages that are currently in use.#
        Then we back cekc each page in th ebuffer if it is currently in use and if not, write to disc and delete it from buffer.
        '''
        running_transactions = self.running_transactions

        # get a list of all pages taht are currently not done
        all_pages_running = []
        for _, pages in running_transactions.items():
            for page in pages:
                all_pages_running.append(page)
        
        # run over each page in buffer and check if it need to be there
        for page_id, page in list(self.buffer.items()):
            if not page_id in all_pages_running:
                print("deleted page from buffer: ",page_id)
                self.__write_data_to_file(page.lsn, page_id, page.user_data)
                self.buffer.pop(page_id)
        
        

    @staticmethod
    def __write_data_to_file(lsn, page_id, data):
        try:
            f = open('pages/page_{}.txt'.format(page_id), "w")
            f.write(data)
            f.close()
        except FileNotFoundError:
            print('File does not exist')

    def __write_log_entry_eot(self, lsn: int, ta_id: int):
        log_entry = f"{lsn},{ta_id},EOT\n"
        self.__write_log_entry(log_entry)

    def __write_log_entry_data(self, lsn: int, ta_id: int, page_id: int, user_data: str):
        log_entry = f"{lsn},{ta_id},{page_id},{user_data}\n"
        self.__write_log_entry(log_entry)

    @staticmethod
    def __write_log_entry(log_entry: str):
        try:
            f = open('log.txt', 'a')
            f.write(log_entry)
            f.close()
        except FileNotFoundError:
            print('File does not exist')
    
    @staticmethod
    def __clear_log_entry():
        ''' Clears the log.txt file on startup '''
        try:
            f = open('log.txt', 'w')
            f.write("")
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
