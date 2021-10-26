# QUERIES
import json
from helper import calSimilarity

def agg_multi_match_q(query, fields=['title','song_lyrics'], operator ='or'):
	q = {
		"size": 500,
		"explain": True,
		"query": {
			"multi_match": {
				"query": query,
				"fields": fields,
				"operator": operator,
				"type": "best_fields"
			}
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
	print(q)
	return q

def agg_multi_match_and_sort_q(query, sort_num, fields=['title','song_lyrics'],comp_op = None, operator ='or'):
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
        "query": {
            "range": {
            "participated_in_parliament": {
                comp_op : sort_num
            }
            }
        },
        "aggs":aggs
        }
	q = json.dumps(q)
	print(q)
	return q

def exact_match(query, required_field, search_val=None):
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
    if search_val:
        q = {
            "size": 500,
            "explain": True,
            "query": {
                "match": {
                    "participated_in_parliament": search_val
                }
            },
            "aggs":aggs
        }
    else:
        search_val = " ".join(calSimilarity(query))
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
    q = json.dumps(q)
    print(q)
    return q