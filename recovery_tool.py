from client import Client
from persistenceManager import PersistenceManager, read_page, write_data_to_file
from multiprocessing import Process

from typing import List, Final

from enum import Enum


class LogEntryType(Enum):
    BOT = 1,
    EOT = 2,
    REDO = 3


class LogEntry:

    type: LogEntryType
    lsn: int
    ta_id: int

    # only for redo
    page_id: int
    user_data: str

    def __init__(self, log_file_entry: str):
        without_new_line = log_file_entry.split('\n')[0]
        split = without_new_line.split(',')
        self.lsn = int(split[0])
        self.ta_id = int(split[1])

        if split[2] == 'BOT':
            self.type = LogEntryType.BOT
        elif split[2] == 'EOT':
            self.type = LogEntryType.EOT
        else:
            self.type = LogEntryType.REDO
            self.page_id = int(split[2])
            self.user_data = split[3]


class RecoveryTool:

    LOG_PATH: Final[str] = 'log.txt'

    def run_recovery(self):
        log_entries = self.__parse_log_file(self.LOG_PATH)
        winning_ta_ids = self.__get_winning_ta_ids(log_entries)
        print("winning transactions: " + str(winning_ta_ids))
        redo_steps = self.__get_redo_steps(log_entries, winning_ta_ids)

        for redo_step in redo_steps:
            if not self.__is_lsn_and_page_already_written(redo_step.page_id, redo_step.lsn):
                print("Recovering page " + str(redo_step.page_id) + " to lsn " + str(redo_step.lsn))
                write_data_to_file(redo_step.lsn, redo_step.page_id, redo_step.user_data)


    @staticmethod
    def __is_lsn_and_page_already_written(page_id: int, lsn: int) -> bool:
        page = read_page(page_id)
        if page is None:
            return False
        return page.lsn >= lsn


    @staticmethod
    def __get_redo_steps(log_entries: List[LogEntry], ta_ids: List[int]) -> List[LogEntry]:
        redo_steps: List[LogEntry] = []
        for log_entry in log_entries:
            if (log_entry.type == LogEntryType.REDO) and (log_entry.ta_id in ta_ids):
                redo_steps.append(log_entry)
        return redo_steps

    @staticmethod
    def __get_winning_ta_ids(log_entries: List[LogEntry]) -> List[int]:
        winning_ta_ids: List[int] = []
        for log_entry in log_entries:
            if log_entry.type == LogEntryType.EOT:
                winning_ta_ids.append(log_entry.ta_id)
        return winning_ta_ids

    @staticmethod
    def __parse_log_file(log_file_path: str) -> List[LogEntry]:
        log_entries: List[LogEntry] = []
        file = open(log_file_path, 'r')
        lines = file.readlines()
        for line in lines:
            log_entries.append(LogEntry(line))
        return log_entries


def main():
    recovery_tool = RecoveryTool()
    recovery_tool.run_recovery()

if __name__ == "__main__":
    main()