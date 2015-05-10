## Code for detecting anomaly

This directory includes the code for detecting anomaly of the traffic in the last week of 2013.

- GenerateThreshold.py: Compute the threshold of every region according to the time period and weather, and save the threshold into a pickle file.
- DetectAnomaly.py: Determine whether a region in a specific time period accoding to the weather is an anomaly compared to the history data.
