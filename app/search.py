# PROCESSING
import re
from lists import stop_words, synonym_list, syn_popularity, times, gte, lte, all_lists, fields_ori, names
from elasticsearch import Elasticsearch, helpers
import queries

client = Elasticsearch(HOST="http://localhost",PORT=9200)
INDEX = 'index-ministers'

def stemmer(word):
    stem_dict = {"ගේ$":"","^(සිටි||හිටි).$":"සිටි","ට$":""}
    for k in stem_dict:
      stemmed = re.sub(k,stem_dict[k],word)
    return stemmed

def preprocess(phrase):
    phrase_l = phrase.split()
    processed_phrase = []
    for word in phrase_l:
      stemmed_word = word
      if not word.isdigit():
        stemmed_word = stemmer(word)
      if stemmed_word not in stop_words:
        processed_phrase.append(stemmed_word)
    processed_s = " ".join(processed_phrase)
    return processed_s

def boost(boost_array):
    # views is not taken for search
    
    name ="name^{}".format(boost_array[1])
    position = "position^{}".format(boost_array[2])
    party = "party^{}".format(boost_array[3])
    district = "district^{}".format(boost_array[4])
    related_subjects = "related_subjects^{}".format(boost_array[5])
    biography = "biography^{}".format(boost_array[6])
    
    return [name, position, party, district, related_subjects, biography]

def searchByName(tokens):
  for token in tokens:
    for name in names:
      if token in name.split():
          print(token)
          return True
  return False

def search_bio(phrase):
    flags = [0, 0, 0, 0, 0, 0, 5]
    fields = boost(flags)
    query_body = queries.agg_multi_match_q(phrase, fields)
    print('Making Faceted Query')
    res = client.search(index=INDEX, body=query_body)
    # res = "biography search"
    return res

def search(phrase):
    # 0 - number
    # 1 - name
    # 2 - position
    # 3 - party
    # 4 - district
    # 5 - related_subjects
    # 6 - biography
    flags = [0, 1, 1, 1, 1, 1, 1]

    #search list
    # 0 - position
    # 1 - party
    # 2 - district
    # 3 - related_subjects
    # 4 - contact info
    # 5 - participation
    search_list = [0, 0, 0, 0, 0, 0]

    num=0
    processed_phrase = preprocess(phrase)
    print(processed_phrase)
    tokens = processed_phrase.split()
    search_by_name = searchByName(tokens)
    containsDigit = bool(re.search(r'\d', processed_phrase))

    if search_by_name:
      flags[1] = 5
      for word in tokens:
        for i in range(len(synonym_list)):
          if word in synonym_list[i]:
            print('Boosting field', i, 'for', word, 'in synonym list - search by name')
            search_list[i] = 1
            break
    elif containsDigit:
      popularity = False
      participation = False
      for word in tokens:
        if word.isdigit():
            flags[0] = 1
            num = int(word)
            print ('Identified sort number',num)
        else:
          if word in syn_popularity:
                popularity = True
          elif word in times:
                op="eql"
                participation = True
                if word in gte:
                  op = 'gte'
                elif word in lte:
                  op = 'lte'
    else:
      # Identify numbers
      for word in tokens:
          

          # Check whether a value from any list is present
          for i in range(len(all_lists)):
              l =  all_lists[i]
              for term in l:
                if word in term.split():
                  print('Boosting field',i+2,'for',word,'in all list')
                  flags[i+2] = 5
                  break

          # Check whether token matches any synonyms
          for i in range(4):
              if word in synonym_list[i]:
                  print('Boosting field', i, 'for', word, 'in synonym list')
                  flags[i+2] = 5

          # Check whether full phrase is in any list - NEED THIS?
          # for i in range(2, 9):
          #     if phrase in all_lists[i]:
          #         print('Boosting field', i, 'for', phrase, 'in all list')
          #         flags[i] = 5
                  
    fields = boost(flags)
    print(processed_phrase, fields, search_list)

    # If the query contain a number call sort query
    phrase = processed_phrase
    if flags[1] == 5:
        required_field = fields_ori[search_list.index(1)]
        print("exact match with "+required_field)
        query_body = queries.exact_match(phrase, required_field)
        res = client.search(index=INDEX, body=query_body)
        res = res['hits']['hits'][0]["fields"][required_field]
    elif flags[0] == 1:
        if popularity:
          print('Making Range Query for popularity')
          query_body = queries.agg_multi_match_and_sort_q(phrase, num, fields)
          res = client.search(index=INDEX, body=query_body)
          resl = res['hits']['hits']
          outputl = []
          for hit in resl:
              outputl.append(hit['_source']['name'])
          res = outputl   
        elif participation:
          if op != "eql":
            print('Making Range Query for participation with '+op)
            query_body = queries.agg_multi_match_and_sort_q(phrase, num, fields, op)
            res = client.search(index=INDEX, body=query_body)
          else:
            print("exact match")
            required_field = "participated_in_parliament"
            query_body = queries.exact_match(phrase, required_field, search_val = num)
            res = client.search(index=INDEX, body=query_body)
          resl = res['hits']['hits']
          outputl = []
          for hit in resl:
              outputl.append(hit['_source']['name'])
          res = outputl 
    else:
        print('Making Faceted Query')
        query_body = queries.agg_multi_match_q(phrase, fields)
        res = client.search(index=INDEX, body=query_body)
        resl = res['hits']['hits']
        outputl = []
        for hit in resl:
            outputl.append(hit['_source']['name'])
        res = outputl 
    print(res)
    return res
