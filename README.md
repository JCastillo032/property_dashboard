# Property Information Dashboard
Dashboard showing data metrics for residential property, such as comparable neighborhood houses recently sold, sales trend for the zip code ﻿94107﻿, and living size/lot size ratios. Uses Python API interaction with ATTOM Real Estate data to display visuals which can be used by buyers before purchasing a home
## Description
#### Frameworks and Languages:
* Python Pandas, Requests
* Power BI PowerQuery
#### Displays relevant information on a property, including:
* Property's detail (number of beds/bath, home/lot sizes, condition of home).
* Comparable home sales including details, within the same zip code.
* Sales Trend for this particular zip code, including average home sale price and number of homes sold.
#### All information is gathered from [ATTOM's Real Estate API](https://api.developer.attomdata.com/home).
#### [Set up your account here](https://api.developer.attomdata.com/signup) to receive your API key and add to API parameter apikey in order to be able to access data. After adding API key, Enable Load to report for all queries.
## Process:
#### Using Python's Requests and Pandas libraries, API calls are made to ATTOM using the parameters' values listed in project. Using Power BI's Python script, end result is data tables used in visuals.
## Parameters:
* web: ATTOM's real estate API site.
* apikey: Add your API key here after you have signed up with ATTOM.
* pAddr: Street address of home to query for, format ex: 123 Main St.
* pCitySt: City and state of home, format ex: Alameda, CA.
* pZip: 5 digit Zip code of home, format ex: 94501.
* pSaleStart: Sale search date to start from, format ex: 2022-08-01.
#
![Property Info Dashboard - Screenshot](https://github.com/JCastillo032/property_dashboard/assets/118695631/2046b926-aec3-4540-88f4-3f3373a1c0e6)
