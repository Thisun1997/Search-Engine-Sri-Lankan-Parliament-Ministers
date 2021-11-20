from elasticsearch import Elasticsearch, helpers
import json

es = Elasticsearch([{'host': 'localhost', 'port':9200}])

def data_upload():
    with open('data/data.json', encoding="utf8") as f:
        data = json.loads(f.read())
    helpers.bulk(es, data, index='index-ministers')
    # print(es.indices.get_mapping())   #print the summary of indices available
    # es.indices.delete(index='index-ministers', ignore=[400, 404])  #delete a created index



if __name__ == "__main__":
    data_upload()