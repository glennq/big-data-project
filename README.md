## Analysis and Visualization of NYC Taxi Data to Find Unusually Busy Areas ##

This is the repository for course project of DS-GA 1004 Big Data.

An online demonstration is accessible at:  http://glennq.github.io/big-data-project/overview.html

Team members:

- Jiyuan Qian
- Yucheng Lu
- Wenjia Wu

The primary goal of our project is to explore New York taxi trip data
from 2011 to 2013, as well as its relationship with the corresponding
weather data. Besides statistics about trips, we focused on retrieving
information about drop-offs and pick-ups at certain location in
certain time under certain weather condition, and detecting anomaly
based on that.

To present our findings, we built a website with visualization that
allows users to choose a day of week, a time period, and a certain
weather type, so that they could explore the distribution of total
number of pick-ups and drop-offs, under the given conditions, by
themselves. We would demon- strate that such visualization and
representation can also be applied to finding regions with unusually
large number of trips, which in turn helps to find unusual events.

Base code for webpages from
https://github.com/mjhea0/thinkful-mentor/tree/master/python/jinja/flask_example
and
https://github.com/twbs/bootstrap/blob/master/docs/examples/dashboard,
used template from https://github.com/IronSummitMedia/startbootstrap-grayscale.

Code for finding regions from https://github.com/ViDA-NYU/aws_taxi.

Built on Bootstrap, Flask and CartoDB.
