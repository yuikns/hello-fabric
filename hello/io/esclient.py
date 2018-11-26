# import json
# import logging
#
# import requests
# from bs4 import UnicodeDammit
#
#
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#
#
# class ESClient(object):
#     def __init__(self, host, port):
#         self.url_base = 'http://%s:%s/' % (host, port)
#         self.url_pub = 'my_index/doc/_search/ '  # 'index_pub/type_pub/_search/'
#         self.url_person = 'index_name/person_11,person_10/_search/'
#         self.url_person_get = 'index_name/person_11/'
#
#     def search_person_by_pub(self, query, aggs=None, filters=None, offset=0, size=30, sort=None):
#         url = self.url_base + "index_name_thin/doc/_search/"
#         print "QUERY ON " + url
#         params = {
#             "from": 0,
#             "size": 0,
#             "fields": [
#                 "_id", "nc", "n"
#             ],
#             "query": {
#                 "query_string": {
#                     "query": "\\'" + query + "\\'~5",
#                     "default_operator": "AND",
#                     "fields": ["t", "a", "n",
#                                "t_alias", "a_alias", "n_alias",
#                                "tok"]
#                 }
#             },
#             "sort": [{"nc": {"order": "desc"}}],
#             "aggs": {
#                 "group_by_org": {
#                     "terms": {
#                         "field": "authors.org",
#                         "size": 100
#                     }
#                 },
#                 "group_by_name": {
#                     "terms": {
#                         "field": "n",
#                         "order": {
#                             "nc_sum": "desc"
#                         },
#                         "size": 1000  # Setting this option too large may leads to cost on network communication
#                     },
#                     "aggs": {
#                         "nc_sum": {
#                             "sum": {
#                                 "script": "log(1+doc['nc'].value) * doc.score + 0.2"
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#         response = requests.post(url, data=json.dumps(params))
#         result = json.loads(UnicodeDammit(response.text).markup)
#         return result
#
#     # People Service
#     def search_person(self, query, aggs=None, filters=None, offset=0, size=30, sort=None):
#         url = self.url_base + "index_name/people2/_search/"
#         params = {
#             "from": offset,
#             "size": size,
#             "query": {
#                 "function_score": {
#                     "query": {
#                         "query_string": {
#                             "fields": ["name", "tags.t", "org"],
#                             "query": query
#                         }
#                     },
#                     "script_score": {
#                         "script": "_score * log(doc['n_pubs'].value + 3) * log(doc['nc'].value + 3)"
#                     }
#                 }
#             }
#         }
#
#         if filters is not None:
#             params["filter"] = filters['filter']
#
#         if sort is not None:
#             if sort == 1:
#                 params["sort"] = [{"nc": {"order": "desc"}}]
#             if sort == 2:
#                 params["sort"] = [{"n_pubs": {"order": "desc"}}]
#
#         if aggs is not None:
#             params["aggs"] = aggs
#
#         response = requests.post(url, data=json.dumps(params))
#         result = json.loads(UnicodeDammit(response.text).markup)
#         return result
#
#     def search_person_facet(self, query, facets):
#         url = self.url_base + 'index_name/people/_search/'
#         params = {
#             "query": {"query_string": {"query": query}},
#             "facets": {}
#         }
#         for f in facets:
#             params["facets"][f] = {
#                 "terms": {
#                     "field": f
#                 }
#             }
#         response = requests.post(url, data=json.dumps(params))
#         result = json.loads(UnicodeDammit(response.text).markup)
#         return result
#
#     def filter_people(self, query, filter):
#         url = self.url_base + 'index_name/people/_search/'
#         params = {
#
#         }
#
#     def facet_person(self, query, facet):
#         url = self.url_base + 'index_name/people/_search/'
#         params = {
#             "query": {"query_string": {"query": query}},
#             "aggs": {
#                 "terms": {
#                     "field": facet
#                 }
#             }
#         }
#         response = requests.post(url, data=json.dumps(params))
#         result = json.loads(UnicodeDammit(response.text).markup)
#         return result
#
#     def get_person_by_id(self, id):
#         self.url_person_get = 'index_name/person_11/'
#         if id[0] == "z":
#             self.url_person_get = 'index_name/person_11/'
#         url = self.url_base + self.url_person_get + id
#         response = requests.get(url)
#         result = json.loads(UnicodeDammit(response.text).markup)
#         return result
#
#     def suggest_person(self, query):
#         url = self.url_base + "index_name_people/_suggest/"
#         print url
#         params = {
#             "name_suggest": {
#                 "text": query,
#                 "completion": {
#                     "field": "suggest"
#                 }
#             }
#         }
#         response = requests.post(url, data=json.dumps(params))
#         result = json.loads(UnicodeDammit(response.text).markup)
#         result = result['name_suggest'][0]['options']
#         return result
#
#     def suggest_topic(self, query):
#         url = self.url_base + "index_name_term/_suggest/"
#         print url
#         params = {
#             "topic_suggest": {
#                 "text": query,
#                 "completion": {
#                     "field": "suggest"
#                 }
#             }
#         }
#         response = requests.post(url, data=json.dumps(params))
#         result = json.loads(UnicodeDammit(response.text).markup)
#         result = result['topic_suggest'][0]['options']
#         for r in result:
#             r["text"] = r["text"].t()
#         return result
#
#     def suggest_pub(self, query):
#         url = self.url_base + "index_name_all_pub/_suggest/"
#         print url
#         params = {
#             "pub_suggest": {
#                 "text": query,
#                 "completion": {
#                     "field": "suggest"
#                 }
#             }
#         }
#         response = requests.post(url, data=json.dumps(params))
#         result = json.loads(UnicodeDammit(response.text).markup)
#         result = result['pub_suggest'][0]['options']
#         for r in result:
#             payload = r["payload"]
#             r["text"] = payload.get("t", "")
#             if not r["text"]:
#                 r["text"] = payload.get("t_alias", "")
#             if not r["text"]:
#                 r["text"] = "Untd"
#         return result
#
#     def suggest_org(self, query):
#         url = self.url_base + "orgrank/_suggest/"
#         print url
#         params = {
#             "org_suggest": {
#                 "text": query,
#                 "completion": {
#                     "field": "suggest"
#                 }
#             }
#         }
#         response = requests.post(url, data=json.dumps(params))
#         result = json.loads(UnicodeDammit(response.text).markup)
#         result = result['org_suggest'][0]['options']
#         return result
#
#     # Publication Service
#     def search_pub(self, query, offset=0, size=20, aggs=None, filters=None, sort=None):
#         url = self.url_base + 'index_name_all_pub/doc/_search/'
#         params = {
#             "from": offset,
#             "size": size,
#             "query": {
#                 "query_string": {
#                     "query": "\"" + query + "\"~" + str(len(query.split(" "))),
#                     "default_operator": "AND",
#                     "fields": ["t", "a", "n", "t_alias", "a_alias", "n_alias"]
#                 }
#             },
#             "highlight": {
#                 "fields": {
#                     "a": {},
#                     "t": {}
#                 }
#             }
#         }
#
#         if filters is not None:
#             print filters
#             params["filter"] = filters['filter']
#             # params["query"]["filtered"]['filter']['range'] = filters['range']
#
#         if aggs is not None:
#             params["aggs"] = aggs
#
#         if sort == "nc":
#             params["sort"] = [{"nc": {"order": "desc"}}]
#         elif sort == "year":
#             params["sort"] = [{"year": {"order": "desc"}}]
#         else:
#             params["sort"] = {
#                 "_script": {
#                     "script":  "log(1+doc['nc'].value) * (10 + doc.score)",
#                     "type": "number",
#                     "order": "desc"
#                 }
#             }
#
#         logging.info("[Search Pub] %s " % json.dumps(params))
#
#         response = requests.post(url, data=json.dumps(params))
#         result = json.loads(UnicodeDammit(response.text).markup)
#
#         return result
#
#     def get_pub_by_ids(self, ids):
#         url = self.url_base + 'index_name/doc/_search/'
#         params = {
#             "query": {
#                 "query_string": {
#                     "query": ' '.join(str(id) for id in ids),
#                     "default_operator": "OR",
#                     "fields": ["_id"]
#                 }
#             }}
#         response = requests.post(url, data=json.dumps(params))
#         result = json.loads(UnicodeDammit(response.text).markup)
#         result = result['hits']['hits']
#         pubs = []
#         for p in result:
#             pubs.append(p['_source'])
#         return pubs
#
#     def get_pub_by_id(self, id):
#         url = self.url_base + 'index_name/doc/_search/'
#         params = {
#             "query": {
#                 "query_string": {
#                     "query": id,
#                     "default_operator": "OR",
#                     "fields": ["_id"]
#                 }
#             }}
#         response = requests.post(url, data=json.dumps(params))
#         print response.text
#         result = json.loads(UnicodeDammit(response.text).markup)
#
#         result = result['hits']['hits'][0]
#         # print result
#         pub = result['_source']
#         return pub
#
#     def warm_up(self, query):
#         url = self.url_base + 'index_name_thin/doc/_search/'
#         params = {
#             "from": 0,
#             "size": 1000,
#             "query": {
#                 "query_string": {
#                     "query": query,
#                     "default_operator": "AND",
#                     "fields": ["t", "a", "t_alias", "a_alias", "n"]
#                 }
#             }
#         }
#
#         response = requests.post(url, data=json.dumps(params))
#         try:
#             result = json.loads(UnicodeDammit(response.text).markup)
#         except:
#             result = {}
#         return result
#
#     def warm_up_expert(self, query, size):
#         url = self.url_base + 'index_name_thin/doc/_search/'
#         params = {
#             "from": 0,
#             "size": 1000,
#             "query": {
#                 "query_string": {
#                     "query": query,
#                     "default_operator": "AND",
#                     "fields": ["t", "a", "t_alias", "a_alias", "n"]
#                 }
#             }
#         }
#         params = {
#             "from": 0,
#             "size": 0,
#             "fields": [
#                 "_id", "nc", "n"
#             ],
#             "query": {
#                 "query_string": {
#                     "query": query,
#                     "default_operator": "AND",
#                     "fields": ["t", "a", "n",
#                                "t_alias", "a_alias", "n_alias", "tok"]}
#             },
#             "sort": [{"nc": {"order": "desc"}}],
#             "aggs": {
#                 "group_by_org": {
#                     "terms": {
#                         "field": "authors.org",
#                         "size": 100
#                     }
#                 },
#                 "group_by_name": {
#                     "terms": {
#                         "field": "n",
#                         "order": {
#                             "nc_sum": "desc"
#                         },
#                         "size": size
#                     },
#                     "aggs": {
#                         "nc_sum": {
#                             "sum": {
#                                 "script": "log(1+doc['nc'].value) * doc.score"
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#         response = requests.post(url, data=json.dumps(params))
#         try:
#             result = json.loads(UnicodeDammit(response.text).markup)
#         except:
#             result = {}
#         return result
#
