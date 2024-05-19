#!/usr/bin/env python3

import logging
import sys

class CustomLogger:

    def __init__(self, logFile, id, fileLevel=logging.DEBUG, consoleLevel=logging.DEBUG):
        self.logger = logging.getLogger(id)
        self.logger.setLevel(logging.DEBUG)

        # Handler that writes in the log file
        file_handler = logging.FileHandler(logFile)
        file_handler.setLevel(fileLevel)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)

        # Handler that writes in the terminal
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(consoleLevel)  
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(console_handler)
