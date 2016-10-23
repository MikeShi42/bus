# UCSD Busses
Sorry this repo is a bit of a mess, I'll be cleaning it up in the 
coming days/weeks!

## State of Code
The python scripts are newer and relatively untested. They suffer from no
exception handling so they just die after running from a couple hours
due to possible malformed API responses. Everything here is hacky and
is not webscale. Primarily due to the lack of MongoDB and Node.js
in this project.

## Files
- `get_bus.py`: Utility functions to fetch bus data, parse it into a named tuple
and append them to a CSV. This file is experimental and suffers from
no exception handling. Not good for long term scraping as it is.
- `scrape_bus_data.py`: Python script that will scrape hard coded bus routes
with certain argument flags to control output and whatnot. Again, it is
experimental and will not work for long term running.
- `curlRoute.sh`: Hits the ucsd bus route API and concatenates to a file.
- `cron5curl.sh`: Calls curlRoute.sh every 5 seconds.
- `parse_flat.py`: Takes a "flat" txt file. This file is generated from
appending API requests to a text file. (cron5curl.sh & curlRoute.sh). It will
then try to split the flat file into daily logs (by looking at the number
of empty API responses and dividing them that way). It's pretty crappy but works.
- `transform_flat_daily.py`: Takes the daily files, parses them and then
puts them all together into a large csv file.
- `1010_1014_out.csv`: Scraped data for Ariba/Nobel UCSD shuttle over the days
of Oct 10th to Oct 14th 2016.

## CSV Data Format
- Updated: When this data point was collected as a unix timestamp
- HasAPC: If this shuttle has APC (automatic people counter) 
- Name: The name of this shuttle. 
- APCPercentage: The load of the shuttle as a percentage (0-100).
- DoorStatus: If the door was open (0 = false, 1 = true) 
- UpdatedAgo: How long ago was this data point given (seconds). 
- Longitude: Longitude of the current shuttle 
- RouteId: Route ID the shuttle is currently on. 
- Heading: The direction the shuttle is heading. 
- IconPrefix: The type of vehicle basically. 
- Latitude: Latitude of the bus. 
- PatternId: Seems like RouteID 
- Speed: The speed of the shuttle, hopefully in MPH 
- ID: The ID of the shuttle (different from name). 
- UpdatedISO: `Updated` but in ISO format. For ease of use in Tableau.
