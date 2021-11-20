# IR_project

## Overview
This repository contains the source code for a search engine developed to search for information about sri lankan parliament ministers. The search engine is built using ElasticSearch and Python.
Folder structre of the repository:
`ES` - contains docker-compose.yml which need to be executed using docker to start the elastic cluster on port 9200
`app` - files/folders related to backend and frontend
- `data` - data scraped from the [website](http://www.manthri.lk/si/politicians)  
- `static` - stylesheets related to frontend
- `template` - html templates related to frontend
- `app.py` - Backend of the web app created using Flask 
- `data_upload.py` - Script to upload data to elastic cluster for indexing
- `helper.py` - helper functions for cosine similarity calculation
- `lists.py` - synonyms and other data utilised for similarity calculations used in query processing
- `queries.py` - elasticsearch queries 
- `search.py` - intent identification and query processing
`queries.txt` - sample queries
`requirements.txt` - package dependancies of the project

## Structure of data
Data of all 224 ministers required for indexing is scrapped from http://www.manthri.lk/si/politicians. Profile of a minister will be stored as a document. All data will be stored in Sinhala. Metadata stored in a document are as follows;
 1.	Name
 2.	position
 3.	party
 4.	district
 5.	contact_information
 6.	related_subjects
 7.	participated_in_parliament – Number of times the minister participated in the parliament.
 8.	overall_rank – rank of the minister based on contribution to the society (calculated by the website)
 9.	biography



Corpus of data scrapped is available [here](/app/data/data.json). The scraper that was used to scrape the website is available [here](https://github.com/Thisun1997/Web-Scraper).

## Indexing and Querying Techniques Used
 *1. Rule based intent classification*
<br>Multiple rules were used to identify the intention of the user and direct them to proper type of searched. Token wise keyword matching between the query and the field values is done using cosine similarity and checked for any synonyms that will describe the intention.
<br>

Eg: If there is a digit in the query, the user intention could be either to search for popular ministers or to search based on their count of participated_in_parliament. If the users’ intention is the prior one, definitely terms like “හොඳම”,” ජනප්රිය” etc. should be there. Based on this term matching, the query is directed to suitable range query.<br>

 *2. Boosting*
<br>Boosting has been used for query optimization. Each field of a search is boosted by a certain value based on the similarity between the keywords and the terms present in the search query.<br>

Eg: If the query contains terms like “තනතුර”, “ධුරය” etc. , “position” field is boosted.

*3.	Tolerate simple spelling errors*
<br>Use cosine similarity to detect correct terms for small spelling errors and retrieve the related search results relavent to corrected version.<br>

Eg: චමල් රාජපක්ෂ මහතාගේ තනතුර and චමල රාපක්ෂ මහතාගේ තනතුර will generate same results


## Main Functionalities
* Match queries – Search for an exact field of a certain minister. (Eg: චමල් රාජපක්ෂ මහතාගේ තනතුර)
* Facetaed queries – Search on the fields position, party, district and related subjects. The query may contain one or two fields for searching. (Eg: සමගි ජන බලවේගය නියෝජනය කරන මන්ත්රීවරු, සමගි ජන බලවේගය නියෝජනය කරන කොළඹ මන්ත්රීවරු).
* Range queries – Searches with ranges on the fields overall_rank and participated_in_parliament. (Eg: හොඳම මන්ත්රීවරු 5 දෙනා , 6 වතාවකට වැඩිය පාර්ලිමේන්තුව නියෝජනය කළ මන්ත්රීවරු )
* Synonyms support – Search phrases support synonyms of the keywords (Eg: using “තනතුර”, “ධුරය” etc. in a query related to the “position” field.
<br>
Following diagram shows the flow IR system utilizing rule based intent classification and boosting to support the above functionalities.<br>

![IR_system_flow](https://user-images.githubusercontent.com/47599759/139177424-f6d7bd9f-1ff4-492d-b94a-085d10da50fc.png)
