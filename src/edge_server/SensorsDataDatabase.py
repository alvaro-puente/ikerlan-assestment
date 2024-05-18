#!/usr/bin/env python3

import sqlite3
import logging
import sys

# Configure log file
logging.basicConfig(filename='/edge_server/logs/sensor_database.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Print logs 
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

class SensorsDataDatabase():
        
    # Connects to database
    def connect(self):
        try:
            # Get connection and cursor
            self.connection = sqlite3.connect('/data/sensors_database.db', check_same_thread=False)
            self.cursor = self.connection.cursor()
            logging.info("Successfully connected to the database.")
        except sqlite3.Error as e:
            logging.error("Error connecting to database: " + str(e))
            raise

    # Adds a new entry in the table
    def addEntry(self, id, name, type, value, timestamp):
        try:
            self.cursor.execute('INSERT INTO sensors_data (id, name, type, value, timestamp) VALUES (?, ?, ?, ?, ?)', (id, name, type, value, timestamp))
            self.connection.commit()
            logging.debug(f"Entry added: ID={id}, Name={name}, Type={type}, Value={value}, Timestamp={timestamp}")
        except sqlite3.Error as e:
            logging.error("Error adding entry to database: " + str(e))
            raise

    # Checks if database has more than numberOfEntries
    def hasNumberOfEntries(self, numberOfEntries):
        try:
            # Count entries
            self.cursor.execute('SELECT COUNT(*) FROM sensors_data')
            count = self.cursor.fetchone()[0]
            logging.debug("Number of entries in database: " + str(count))
            return count > numberOfEntries
        except sqlite3.Error as e:
            logging.error("Error counting entries in database: " + str(e))
            raise

    # Return numberOfEntries id, value pairs
    def obtainNumberOfEntriesValues(self, numberOfEntries):
        try:
            self.cursor.execute('SELECT id, value FROM sensors_data LIMIT ?', (numberOfEntries,))
            results = self.cursor.fetchall()
            logging.debug("Obtained " + str(len(results)) + " entries from database.")
            return results
        except sqlite3.Error as e:
            logging.error("Error retrieving entries from database: " + str(e))
            raise
    
    # Delete the number of entries given by the ids array
    def deleteEntriesById(self, ids):
        try:
            self.cursor.execute('DELETE FROM sensors_data WHERE id IN ({seq})'.format(seq=','.join(['?']*len(ids))), ids)
            self.connection.commit()
            logging.debug("Deleted entries with IDs: " + str(ids))
        except sqlite3.Error as e:
            logging.error("Error deleting entries from database: " + str(e))
            raise

