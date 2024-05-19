#!/usr/bin/env python3

from CustomLogger import CustomLogger
import mysql.connector

procLogger = CustomLogger('/edge_server/logs/processed_database.log', "processed_database")

class ProcessedDataDatabase():
        
    # Connect to database
    def connect(self):
        try:
            # Connect to MySQL database
            self.connection = mysql.connector.connect(
                host='10.5.0.8',
                port='3306',
                user='root',
                password='rootpassword',
                database='processed_database'
            )
            self.cursor = self.connection.cursor()
            procLogger.logger.info("Successfully connected to the database.")
        except mysql.connector.Error as e:
            procLogger.logger.error("Error connecting to database: " + str(e))
            raise

    # Adds a new entry in the table
    def addEntry(self, id, value):
        try:
            self.cursor.execute('INSERT INTO processed_data (id, value) VALUES (%s, %s)', (id, value))
            self.connection.commit()
            procLogger.logger.debug(f"Entry added: ID={id}, Value={value}")
        except mysql.connector.Error as e:
            procLogger.logger.error("Error adding entry to database: " + str(e))
            raise
