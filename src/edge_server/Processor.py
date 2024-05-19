#!/usr/bin/env python3

from CustomLogger import CustomLogger
import numpy as np

processorLogger = CustomLogger('/edge_server/logs/processor.log', "processor")

"""
This class provides all the relevant methods to filter data
"""
class Processor():
    
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