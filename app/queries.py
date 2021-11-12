# QUERIES
import json
from helper import calSimilarity

def agg_multi_match_q(query, fields, operator ='and'):
	if operator == 'or':
		multi_match_q = {
				"query": query,
				"fields": fields,
				"operator": operator,
				"type": "best_fields",
				"fuzziness" : "AUTO"
			}
	else:
		multi_match_q = {
				"query": query,
				"fields": fields,
				"operator": operator,
				"type": "best_fields"
			}		
	q = {
		"size": 500,
		"explain": True,
		"query": {
			"multi_match": multi_match_q
		},
		"aggs": {
			"Position Filter": {
				"terms": {
					"field": "position.keyword",
					"size": 10
				}
			},
			"Party Filter": {
				"terms": {
					"field": "party.keyword",
					"size": 10
				}
			},
			"District Filter": {
				"terms": {
					"field": "district.keyword",
					"size": 10
				}
			},
			"Related Subjects Filter": {
				"terms": {
					"field": "related_subjects.keyword",
					"size": 10
				}
			},
      		"Biography Filter": {
				"terms": {
					"field": "biography.keyword",
					"size": 10
				}
			}
		}
	}

	q = json.dumps(q)
	
	return q

def agg_multi_match_and_sort_q(sort_num,comp_op = None):
	print ('sort num is ',sort_num)
	aggs = {
			"Position Filter": {
				"terms": {
					"field": "position.keyword",
					"size": 10
				}
			},
			"Party Filter": {
				"terms": {
					"field": "party.keyword",
					"size": 10
				}
			},
			"District Filter": {
				"terms": {
					"field": "district.keyword",
					"size": 10
				}
			},
			"Related Subjects Filter": {
				"terms": {
					"field": "related_subjects.keyword",
					"size": 10
				}
			}
		}
	if comp_op == None:
		q =  {
        "size": sort_num,
        "sort": [
            {"overall_rank": {"order": "asc"}},
        ],
        "query": {
            "match_all" : {}
        },
        "aggs":aggs
        }
	else:
		q = {
		"size":500,
        "query": {
            "range": {
            "participated_in_parliament": {
                comp_op : sort_num
            }
            }
        },
        # "aggs":aggs
        }
	q = json.dumps(q)
	
	return q

def exact_match(query, required_field=None, search_val=None):
    if search_val:
        q = {
            "size": 500,
            "explain": True,
            "query": {
                "match": {
                    "participated_in_parliament": search_val
                }
            },
        }
    else:
        search_val = " ".join(calSimilarity(query))
        if required_field:
        	q = {
				"size": 500,
				"explain": True,
				"query": {
					"match": {
						"name": search_val
					}
				},
				"fields" : [required_field]
			}
        else:
        	q = {
				"size": 500,
				"explain": True,
				"query": {
					"match": {
						"name": search_val
					}
				},
			}
    q = json.dumps(q)
    
    return q