## Code for MapReduce

This directory includes code for running MapReduce jobs on AWS.

- rtree.sh: bash script for bootstrapping EMR nodes
- density\_hourly: Computing total number of trips grouped by hours in any day.
- density\_regions: Finding regions where the number of trips is always large or small.
- density\_weekend\_weekday: Number of trips grouped by day of week. Used to find daily number of trips for weekends and weekdays respectively.
- region\_distribution: To get counts of trips grouped by day of week, time of day, and region.
- trip\_total\_hourly: Used to find hourly number of trips for all 24 * 365 hours.
