from PyQt5.QtWidgets import QApplication
import argparse
import logging
import sys, time
from analyzer import Analyzer

if __name__ == '__main__':
    log_folder = 'D:/Project/wAnalyzer2/log/'
    log_file = time.strftime('%Y%m%d_log.txt')

    parser = argparse.ArgumentParser(description='argument description')
    parser.add_argument('--log', required=False, default='debug', help='logging level')
    parser.add_argument('--key', required=True, help='raw key')
    args = parser.parse_args()
    log_level = args.log.upper()
    key = args.key

    # console_formatter = logging.Formatter('\033[33m%(funcName)s (line: %(lineno)s)\n\033[31m%(levelname)s \033[30m%(message)s\033[0m')
    console_formatter = logging.Formatter('\033[91m%(levelname)s \033[97m%(message)s\033[0m')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    file_formatter = logging.Formatter('%(asctime)s %(message)s')
    file_handler = logging.FileHandler(log_folder+log_file, mode='w')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    log = logging.getLogger('kiwoom')
    log.addHandler(console_handler)
    log.addHandler(file_handler)
    log.setLevel(log_level)

    app = QApplication(sys.argv)
    analyzer = Analyzer(log, key)
    app.exec()