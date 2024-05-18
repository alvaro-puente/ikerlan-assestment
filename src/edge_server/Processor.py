#!/usr/bin/env python3

import numpy as np
import logging
import sys

# Configure log file
logging.basicConfig(filename='/edge_server/logs/processor.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Print logs 
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

"""
This class provides all the relevant methods to filter data
"""
class Processor():
    
    # Outlier filters
    def applyOutliersFilter(data):
        try:
            logging.info("Starting filtering process")
            # If len is less than 1 this filter cannot be applied
            if len(data) < 2:
                logging.info("Filter process stopped due to insufficient data numbers")
                return data
            logging.debug("Number data filtered: " + str(len(data)))
            logging.debug("Data numbers: " + str(data))
            # Calculate mean, variance and standart deviation
            mean = sum(data) / len(data)
            variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
            std = variance ** 0.5
            # Calculate max and minimum limits
            low = mean - 3 * std
            high = mean + 3 * std
            logging.debug("Max limit: " + str(high))
            logging.debug("Min limit: " + str(low))
            # Filter 
            filteredValues = [v if low <= v <= high else np.nan for v in data]
            filteredValuesWithNoNaNVAlues = [v for v in filteredValues if not np.isnan(v)]
            logging.debug("Data filtered: " + filteredValuesWithNoNaNVAlues)
            logging.info("Filtering was done correctly")
            return filteredValuesWithNoNaNVAlues
        except Exception as e:
            logging.error("An error has occurred when filtering: " + str(e))