# IR_project

## Overview
This repository contains the source code for a search engine developed to search for information about sri lankan parliament ministers. The search engine is built using ElasticSearch and Python.

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



Corpus of data scrapped is available [here](/app/data/data.json). The crawler that was used to scrape the website is available here.

## Indexing and Querying Techniques Used
 *1. Rule based intent classification*
<br>Multiple rules were used to identify the intention of the user and direct them to proper type of searched. Token wise keyword matching between the query and the field values is done using cosine similarity and checked for any synonyms that will describe the intention.
<br>

Eg: If there is a digit in the query, the user intention could be either to search for popular ministers or to search based on their count of participated_in_parliament. If the users’ intention is the prior one, definitely terms like “හොඳම”,” ජනප්රිය” etc. should be there. Based on this term matching, the query is directed to suitable range query.<br>

 *2. Boosting*
<br>Boosting has been used for query optimization. Each field of a search is boosted by a certain value based on the similarity between the keywords and the terms present in the search query.<br>

Eg: If the query contains terms like “තනතුර”, “ධුරය” etc. , “position” field is boosted.

## Main Functionalities
* Match queries – Search for an exact field of a certain minister. (Eg: චමල් රාජපක්ෂ මහතාගේ තනතුර)
* Facetaed queries – Search on the fields position, party, district and related subjects. (Eg: සමගි ජන බලවේගය නියෝජනය කරන මන්ත්රීවරු)
* Range queries – Searches with ranges on the fields overall_rank and participated_in_parliament. (Eg: හොඳම මන්ත්රීවරු 5 දෙනා , 6 වතාවකට වැඩිය පාර්ලිමේන්තුව නියෝජනය කළ මන්ත්රීවරු )
* Synonyms support – Search phrases support synonyms of the keywords (Eg: using “තනතුර”, “ධුරය” etc. in a query related to the “position” field.
<br>
Following diagram shows the flow IR system utilizing rule based intent classification and boosting to support the above functionalities.<br>

![IR_system_flow](https://user-images.githubusercontent.com/47599759/139177424-f6d7bd9f-1ff4-492d-b94a-085d10da50fc.png)
