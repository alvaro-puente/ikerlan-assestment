#!/usr/bin/env python3

from ProcessedDataDatabase import ProcessedDataDatabase
from SensorsDataDatabase import SensorsDataDatabase
from CustomLogger import CustomLogger
import numpy as np
import uuid

processorLogger = CustomLogger('/edge_server/logs/processor.log', "processor")

"""
This class provides all the relevant methods to process data
"""
class Processor():

    def __init__(self):
        # Connect to databases
        self.sensorsDataDatabase = SensorsDataDatabase()
        self.sensorsDataDatabase.connect()
        self.processedDataDatabase = ProcessedDataDatabase()
        self.processedDataDatabase.connect()

    # Store message in database
    def processMessage(self, message):
        # Store message
        self.storeMessage(message)
        # Check if database reaches more than numberOfEntries
        numberOfEntries = 50
        hasNumberEntries = self.sensorsDataDatabase.hasNumberOfEntries(numberOfEntries)
        # If reaches...
        if hasNumberEntries:
            # Process data entries
            self.applyProcessing(numberOfEntries)

    # Store message in database
    def storeMessage(self, message):
        id = str(uuid.uuid4())
        name = message["sensor_id"]
        type = message["sensor_type"]
        value = message["value"]
        timestamp = message["timestamp"]
        self.sensorsDataDatabase.addEntry(id, name, type, value, timestamp)
        
    # Process the message
    def applyProcessing(self, numberOfEntries):
        # Get numberOfentries number of values to be processed
        idValuePairs = self.sensorsDataDatabase.obtainNumberOfEntriesValues(numberOfEntries)
        ids = [row[0] for row in idValuePairs]
        values = [row[1] for row in idValuePairs]
        # Process values and store them in a new database
        processedValues = self.applyOutliersFilter(values)
        for value in processedValues:
            id = str(uuid.uuid4())
            self.processedDataDatabase.addEntry(id, value)
        # Delete processed values from database
        self.sensorsDataDatabase.deleteEntriesById(ids)

    # Outlier filters
    def applyOutliersFilter(self, data):
        try:
            processorLogger.logger.info("Starting filtering process")
            # If len is less than 1 this filter cannot be applied
            if len(data) < 2:
                processorLogger.logger.info("Filter process stopped due to insufficient data numbers")
                return data
            processorLogger.logger.debug("Number data filtered: " + str(len(data)))
            processorLogger.logger.debug("Data numbers: " + str(data))
            # Convert values to int (they are stored as string in the database)
            data = [float(value) for value in data]
            # Calculate mean, variance and standart deviation
            mean = sum(data) / len(data)
            variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
            std = variance ** 0.5
            processorLogger.logger.debug("Mean: " + str(mean))
            processorLogger.logger.debug("Variance: " + str(variance))
            processorLogger.logger.debug("Std: " + str(std))
            # Calculate max and minimum limits
            low = mean - 3 * std
            high = mean + 3 * std
            processorLogger.logger.debug("Max limit: " + str(high))
            processorLogger.logger.debug("Min limit: " + str(low))
            # Filter 
            filteredValues = [v if low <= v <= high else np.nan for v in data]
            filteredValuesWithNoNaNValues = [v for v in filteredValues if not np.isnan(v)]
            processorLogger.logger.debug("Data filtered: " + str(filteredValuesWithNoNaNValues))
            processorLogger.logger.info("Filtering was done correctly. Eliminated " + str(len(data)-len(filteredValuesWithNoNaNValues)) + " values")
            return filteredValuesWithNoNaNValues
        except Exception as e:
            processorLogger.logger.error("An error has occurred when filtering: " + str(e))