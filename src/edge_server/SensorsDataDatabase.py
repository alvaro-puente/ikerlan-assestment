#!/usr/bin/env python3

from CustomLogger import CustomLogger
import mysql.connector

sensLogger = CustomLogger('/edge_server/logs/sensors_database.log', "sensors_database")

class SensorsDataDatabase():
        
    # Connects to database
    def connect(self):
        try:
            # Connect to MySQL database
            self.connection = mysql.connector.connect(
                host='10.5.0.8',
                port='3306',
                user='root',
                password='rootpassword',
                database='sensors_database'
            )
            self.cursor = self.connection.cursor()
            sensLogger.logger.info("Successfully connected to the database.")
        except mysql.connector.Error as e:
            sensLogger.logger.error("Error connecting to database: " + str(e))
            raise

    # Adds a new entry in the table
    def addEntry(self, id, name, type, value, timestamp):
        try:
            self.cursor.execute('INSERT INTO sensors_data (id, name, type, value, timestamp) VALUES (%s, %s, %s, %s, %s)', (id, name, type, value, timestamp))
            self.connection.commit()
            sensLogger.logger.debug(f"Entry added: ID={id}, Name={name}, Type={type}, Value={value}, Timestamp={timestamp}")
        except mysql.connector.Error as e:
            sensLogger.logger.error("Error adding entry to database: " + str(e))
            raise

    # Checks if database has more than numberOfEntries
    def hasNumberOfEntries(self, numberOfEntries):
        try:
            # Count entries
            self.cursor.execute('SELECT COUNT(*) FROM sensors_data')
            count = self.cursor.fetchone()[0]
            sensLogger.logger.debug("Number of entries in database: " + str(count))
            return count > numberOfEntries
        except mysql.connector.Error as e:
            sensLogger.logger.error("Error counting entries in database: " + str(e))
            raise

    # Return numberOfEntries id, value pairs
    def obtainNumberOfEntriesValues(self, numberOfEntries):
        try:
            self.cursor.execute('SELECT id, value FROM sensors_data LIMIT %s', (numberOfEntries,))
            results = self.cursor.fetchall()
            sensLogger.logger.debug("Obtained " + str(len(results)) + " entries from database.")
            return results
        except mysql.connector.Error as e:
            sensLogger.logger.error("Error retrieving entries from database: " + str(e))
            raise
    
    # Delete the number of entries given by the ids array
    def deleteEntriesById(self, ids):
        try:
            self.cursor.execute('DELETE FROM sensors_data WHERE id IN (%s)' % ','.join(['%s']*len(ids)), ids)
            self.connection.commit()
            sensLogger.logger.debug("Deleted entries with IDs: " + str(ids))
        except mysql.connector.Error as e:
            sensLogger.logger.error("Error deleting entries from database: " + str(e))
            raise