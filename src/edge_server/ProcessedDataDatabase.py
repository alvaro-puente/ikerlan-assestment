#!/usr/bin/env python3

import sqlite3
import logging
import sys

# Configure log file
logging.basicConfig(filename='/edge_server/logs/processed_sensors.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Print logs 
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

class SensorsDataDatabase():
        
    # Connect to database
    def connect(self):
        try:
            # Get connection and cursor
            self.connection = sqlite3.connect('processed_sensors.db', check_same_thread=False)
            self.cursor = self.connection.cursor()
            logging.info("Successfully connected to the database.")
        except sqlite3.Error as e:
            logging.error("Error connecting to database: " + str(e))
            raise

    # Adds a new entry in the table
    def addEntry(self, id, value):
        try:
            self.cursor.execute('INSERT INTO processed_data (id, value) VALUES (?, ?)', (id, value))
            self.connection.commit()
            logging.info(f"Entry added: ID={id}, Value={value}")
        except sqlite3.Error as e:
            logging.error("Error adding entry to database: " + str(e))
            raise