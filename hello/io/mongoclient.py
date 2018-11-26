import time

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import re


# http://api.mongodb.com/python/current/tutorial.html
class MongoAgent(object):
    def __init__(self, host, port, dbname, username, password):
        self.db = MongoClient(host, port)[dbname]
        if username != "" and password != "":
            self.db.authenticate(username, password)

        self.calls_col = self.db["calls"]
        self.segments_col = self.db["segments"]
        self.sentences_col = self.db["sentences"]

    def iter_all(self, c, handler):
        for doc in c.find():
            if not handler(doc):
                break

    def find_one_by_key_value(self, c, key, value):
        return c.find_one({key : value})

    def coll(self, name):
        return self.db[name]

# def get_persons_by_pubs(self, pubs):
#         return self.person_col.find({
#             "$or": [{"pubs": {"$elemMatch": {"i": p["i"], "r": int(p["o"])}}} for p in pubs]
#         })
#
#     def get_persons_by_pids(self, pids):
#         return self.person_col.find({
#             "$or": [{"pubs.i": p} for p in pids]
#         })
#
#     # Author Service
#     def get_person_by_id(self, _id):
#         result = self.person_col.find_one({"_id": ObjectId(_id)})
#         return result
#
#     def get_person(self, name):
#         result = self.person_col.find_one({"names": name})
#         return result
#
#     def insert_person(self, data):
#         _id = self.person_col.insert(data)
#         return str(_id)
#
#     def update_person(self, _id, data):
#         self.person_col.update({"_id": ObjectId(_id)}, {"$set": data})
#         return True
#
#     def delete_persons(self, _ids):
#         self.person_col.remove({"_id": {"$in": [ObjectId(id) for id in _ids]}})
#
#     def get_persons(self, _ids):
#         result = self.person_col.find({"_id": {"$in": [ObjectId(id) for id in _ids]}})
#         return result
#
#     def get_persons_new_reviewer(self, _ids):
#         result = self.person_col.find({"_id": {"$in": [ObjectId(id) for id in _ids]}, "reviewer": 1})
#         return result
#
#     def get_persons_only_name(self, _ids):
#         result = self.person_col.find({"_id": {"$in": [ObjectId(id) for id in _ids]}}, {"names": 'true'})
#         return result
#
#     def get_person_by_nsfc_id(self, nid):
#         result = self.person_col.find_one({"nsfc": nid})
#         return result
#
#     def get_person_pub_ids(self, pid):
#         result = self.person_col.find_one({"_id": ObjectId("53c81facdabfae51bb115f14")}, {"pubs.i": 1})
#         return [x["i"] for x in result.get("pubs", [])]
#
#     def get_all_person(self):
#         result = self.person_col.find({})
#         return result
#
#     def save_person(self, item):
#         self.person_col.save(item)
#
#     # Publication Service
#     def get_pubs(self, _ids, count=None, year=None, order=1, offset=0):
#         if year is not None:
#             return self.pub_col.find(
#                 {"$and": [
#                     {"_id": {"$in": [ObjectId(id) for id in _ids]}},
#                     {"year": year}
#                 ]
#                 })
#         elif count is not None:
#             return self.pub_col.find({"_id": {"$in": [ObjectId(id) for id in _ids]}}).sort("year", -1).skip(
#                 offset).limit(count)
#         if order == 1:
#             return self.pub_col.find({"_id": {"$in": [ObjectId(id) for id in _ids]}}).sort("year", -1)
#         elif order == 0:
#             return self.pub_col.find({"_id": {"$in": [ObjectId(id) for id in _ids]}})
#
#     def get_pub(self, _id):
#         return self.pub_col.find_one({"_id": ObjectId(_id)})
#
#     def get_pub_type(self, _id):
#         publication = self.pub_col.find_one({"_id": ObjectId(_id)})
#         print "xiangyu"
#         venue_type = publication.get('venue', {})
#         if venue_type.get("type"):
#             # return venue_type["type"]
#             if venue_type["type"] == 0:
#                 return "inproceedings"
#             elif venue_type["type"] == 1:
#                 return "journals"
#             elif venue_type["type"] == 2:
#                 return "conference"
#             elif venue_type["type"] == 3:
#                 return "book"
#             elif venue_type["type"] == 4:
#                 return "thesis"
#             elif venue_type["type"] == 5:
#                 return "technical report"
#             elif venue_type["type"] == 6:
#                 return "encyclopedia"
#             elif venue_type["type"] == 7:
#                 return "magazine"
#             elif venue_type["type"] == 8:
#                 return "newsletter"
#             elif venue_type["type"] == 9:
#                 return "play"
#             elif venue_type["type"] == 10:
#                 return "inproceedings"
#             elif venue_type["type"] == 11:
#                 return "article"
#             elif venue_type["type"] == 12:
#                 return "incollection"
#             else:
#                 return "WWW"
#         else:
#             return "inproceedings"
#
#     def get_all_pubs(self):
#         return self.pub_col.find({})
#
#     def get_all_pubs_lang(self, lang):
#         return self.pub_col.find({"lang": lang})
#
#     def get_pubs_with_pid_src(self, _pids, src):
#         result = self.pub_col.find({"pid": {"$in": [ObjectId(pid) for pid in _pids]}, "src": src})
#         return result
#
#     def get_terms(self):
#         return self.term_col.find()
#
#     # #xiangyu  get post information function
#     def get_post_by_id(self, id):
#         result = self.post_col.find_one({"_id": ObjectId(id)})
#         return result
#
#     def get_post_for_paper(self, id):
#         result = self.post_col.find({"paper_id": ObjectId(id)}).sort("time", -1)
#         return result
#
#     def get_social_info(self, id):
#         result = self.in_followed.find_one({"target": ObjectId(id)})
#         return result
#
#     def get_user_info(self, id):
#         result = self.out_following.find_one({"src": ObjectId(id)})
#         return result
#
#     def get_binding_info(self, id):
#         user = self.usr_col.find_one({"_id": ObjectId(id)}, {"link": 1})
#         return user["link"]
#
#     def get_author_binding(self, id):
#         author = self.usr_col.find_one({"link": id}, {"link": 1})
#         if author:
#             return True
#         else:
#             return False
#
#     ##get user connection
#     def get_user_connection(self, id):
#         following_people = self.out_following.find_one({"src": ObjectId(id)}, {"target": 1, "_id": 0})
#         following_id = []
#         if following_people:
#             for target in following_people['target']:
#                 if target['type'] == 'people':
#                     following_id.append(target['id'])
#         return following_id
#
#     def get_user_following_by_size(self, id, offset, size):
#         following_people = self.out_following.find_one({"src": ObjectId(id)}, {"target": 1, "_id": 0})
#         following_id = []
#         if following_people:
#             for target in following_people['target']:
#                 if target['type'] == 'people':
#                     following_id.append(target['id'])
#         show_id = []
#         for num in range(offset, offset + size):
#             if num == len(following_id):
#                 break
#             show_id.append(following_id[num])
#         return show_id
#
#     def get_user_follower_by_size(self, id, offset, size):
#         follower_people = self.in_followed.find_one({"target": ObjectId(id)}, {"src": 1, "_id": 0})
#         follower_id = []
#         if follower_people:
#             for src in follower_people['src']:
#                 follower_id.append(src['id'])
#         show_id = []
#         for num in range(offset, offset + size):
#             if num == len(follower_id):
#                 break
#             show_id.append(follower_id[num])
#         return show_id
#
#     def get_user_follower(self, id):
#         follower_people = self.in_followed.find_one({"target": ObjectId(id)}, {"src": 1, "_id": 0})
#         follower_id = []
#         if follower_people:
#             for src in follower_people['src']:
#                 follower_id.append(src['id'])
#         return follower_id
#
#     ## xiangyu  update reply for a post
#     def update_replyToPost(self, post_id, reply_time, name, content):
#         try:
#             status = self.post_col.update(
#                 {"_id": ObjectId(post_id)},
#                 {"$push": {"reply": {'name': name, 'content': content, 'reply_time': reply_time}}}
#             )
#
#         except Exception as e:
#             return False, str(e)
#
#     ## xiangyu:add api to delete reply of post, may need add id???
#     def delete_reply_of_post(self, post_id, reply_time):
#         try:
#             status = self.post_col.update(
#                 {"_id": ObjectId(post_id)},
#                 {"$pull": {"reply": {"reply_time": reply_time}}}
#             )
#         except Exception as e:
#             return False, str(e)
#
#     ## get social status
#     def get_social_status(self, id, people):
#         if self.get_user_info(id):
#             followling_list = self.get_user_info(id)
#             follow = []
#             for person in people:
#                 for folling_people in followling_list['target']:
#                     if person['id'] == folling_people['id']:
#                         follow.append(person['id'])
#                         break
#             return follow
#         else:
#             return []
#
#     def judge_following_status(self, id, people_id):
#         if self.get_user_info(id):
#             followling_list = self.get_user_info(id)
#             print followling_list
#             for folling_people in followling_list['target']:
#                 if people_id == folling_people['id']:
#                     return True
#             return False
#         return False
#         # return 1
#
#     ## delete following people
#     def delete_following_people(self, id, following_id):
#         try:
#             people_collection_delete = self.in_followed.update(
#                 {"target": ObjectId(following_id)}, {"$pull": {"src": {'id': id}}}
#             )
#             user_collection_delete = self.out_following.update(
#                 {"src": ObjectId(id)}, {"$pull": {"target": {"id": following_id}}}
#             )
#             return "delete"
#         except Exception as e:
#             return False, str(e)
#
#     def add_following_people(self, id, following_id, time, type):
#         try:
#             in_src = {'id': id, 'time': time}
#             out_src = {'id': following_id, 'time': time, 'type': type}
#
#             if self.get_social_info(following_id):
#                 _following_info = self.in_followed.update(
#                     {"target": ObjectId(following_id)}, {"$push": {"src": in_src}}
#                 )
#             else:
#                 _following_id = self.in_followed.insert({
#                     "target": ObjectId(following_id),
#                     "src": [in_src],
#                     "type": type
#                 })
#
#             if self.get_user_info(id):
#                 _user_info = self.out_following.update(
#                     {"src": ObjectId(id)}, {"$push": {"target": out_src}}
#                 )
#             else:
#                 _user_id = self.out_following.insert({
#                     "src": ObjectId(id),
#                     "target": [out_src],
#                 })
#             result = self.get_social_info(following_id)
#             if result:
#                 return True, "success"
#             else:
#                 return False, 'insert failed'
#         except Exception as e:
#             return False, str(e)
#
#     def add_post(self, paper_id, time, name, content):
#         try:
#             _post_id = self.post_col.insert({
#                 "paper_id": ObjectId(paper_id),
#                 "time": time,
#                 "name": name,
#                 "content": content,
#                 "reply": []
#             })
#
#             print "post_id :", _post_id
#             result = self.get_post_by_id(_post_id)
#             if result:
#                 return True, "success"
#             else:
#                 return False, "insert failed"
#         except Exception as e:
#             return False, str(e)
#
#     def add_log(self, uid, id, event, field, pre, post):
#         uid = session.get('id', None)
#         uname = session.get('uname', None)
#         email = session.get('email', None)
#         log_ip = get_remote_ip()
#         self.log_col.save({"uid": uid,
#                            "uname": uname,
#                            "pid": id,
#                            "event": event,
#                            "field": field,
#                            "pre": pre,
#                            "ip": log_ip,
#                            "time": time.time(),
#                            "email": email,
#                            "post": post})
#
#     def read_all_log(self):
#         self.log_col.find({})
#
#     def read_log(self, src_offset, length):
#         if src_offset < 0:
#             src_offset = 0
#         diff = 86400.0  # one day's difference
#         current_time = time.time()
#         src_time = current_time - diff * src_offset
#         if length == -1:
#             result = self.log_col.find({"time": {"$lte": src_time}}).sort("_id", pymongo.DESCENDING)
#         else:
#             dest_time = src_time - diff * length
#             result = self.log_col.find({"time": {"$gte": dest_time, "$lte": src_time}}).sort("_id", pymongo.DESCENDING)
#         return result
#
#     # User Service
#     # userid
#     # username
#     # email
#     # password # md5ed
#     # role :    0: only several experts
#     # 1: several division
#     #           2: admin
#     # experts : experts list
#     # div : division
#     # def add_usr(self,id,name,email,password,role,experts,div):
#     #    self.usr_col.save({"id":id,
#     #                        "name":name,
#     #                        "email":email,
#     #                        "password":passord,
#     #                        "role":role,
#     #                        "experts":experts,
#     #                        "div":div})
#
#     def add_user(self, name, fname, lname, email=None, password=None, gender=2, role=0, link=None, title=7, address="",
#                  org="", sub=False,
#                  temp_token=""):
#         if not name or not email:
#             return False, "name or email is empty ..."
#         gender_str = GENDER_DICT.get(gender, None)
#         title_str = TITLE_DICT.get(title, None)
#         print "[mongoclinet$add_user] remote ip ", get_remote_ip()
#         try:
#             _rid = self.usr_col.insert({
#                 "name": name,
#                 "fname": fname,
#                 "lname": lname,
#                 "gender": gender_str,
#                 "email": email,
#                 "pass": password,
#                 "role": role,
#                 "link": link,
#                 "title": title_str,
#                 "addr": address,
#                 "org": org,
#                 "sub": sub,
#                 "reg_ip": get_remote_ip(),
#                 "reg_time": time.time(),
#                 "temp_token": temp_token
#             })
#             print "rid :", _rid
#             result = self.get_usr_by_id(_rid)
#             # print "judge :",judge is not None
#             # return  judge is not None
#             if result:
#                 return True, "success"
#             else:
#                 if self.get_usr_by_name(name):
#                     return False, "name already found"
#                 if self.get_usr_by_email(email):
#                     return False, "email already found"
#                 return False, "insert failed"
#         except Exception as e:
#             return False, str(e)
#
#     def set_usr_temp_token_by_id(self, id, temp_token):
#         temp_token = temp_token.strip()
#         try:
#             user_item = self.get_usr_by_id(id)
#             if user_item:
#                 self.usr_col.update({"_id": ObjectId(user_item["_id"])}, {"$set": {"temp_token": temp_token}})
#                 return True
#             return False
#         except:
#             return False
#
#     def set_usr_temp_token_by_name(self, name, temp_token):
#         temp_token = temp_token.strip()
#         try:
#             user_item = self.get_usr_by_name(name)
#             if user_item:
#                 self.usr_col.update({"_id": ObjectId(user_item["_id"])}, {"$set": {"temp_token": temp_token}})
#                 return True
#             return False
#         except:
#             return False
#
#     def update_usr_password_by_id(self, id, password):
#         if password:
#             user_item = self.get_usr_by_id(id)
#             if user_item:
#                 self.usr_col.update({"_id": ObjectId(user_item["_id"])}, {"$set": {"pass": password}})
#                 return True
#             return False
#         else:
#             return False
#
#     def update_usr_temp_token_by_name(self, name, temp_token):
#         user_item = self.get_usr_by_name(name)
#         if user_item:
#             self.usr_col.update({"_id": ObjectId(user_item["_id"])}, {"$set": {"temp_token": temp_token}})
#             return True
#         return False
#
#     def update_usr_link_by_id(self, uid, pid):
#         person = None
#         if pid:
#             person = self.get_person_by_id(pid)
#         if person or not pid:
#             user_item = self.get_usr_by_id(uid)
#             if user_item:
#                 self.usr_col.update({"_id": ObjectId(uid)}, {"$set": {"link": pid}})
#                 return True, "updated"
#             return False, "no such user"
#         else:
#             return False, "no such person"
#
#     def get_usr_by_id(self, id):
#         result = self.usr_col.find_one({"_id": ObjectId(id)})
#         return result
#
#     def get_usr_by_name(self, name):
#         result = self.usr_col.find_one({"name": name})
#         return result
#
#     def get_usr_by_email(self, email):
#         result = self.usr_col.find_one({"email": email})
#         return result
#
#     def del_usr_by_id(self, id):
#         return self.usr_col.remove({"_id": ObjectId(id)}, 1)
#
#     # Publication Service
#     def get_Orgrank(self, domain, isAcademic):
#         if int(isAcademic) == 3:
#             return self.orgrank_col.find({}, {"org": 1, "idorg": 1, "typeScore": {'$slice': [int(domain), 1]}})
#         else:
#             return self.orgrank_col.find({"type": isAcademic},
#                                          {"org": 1, "idorg": 1, "typeScore": {'$slice': [int(domain), 1]}})
#
#     def search_org(self, query, isAcademic):
#         if int(isAcademic) == 3:
#             return self.orgrank_col.find({"orgClusterText": {'$regex': re.compile(query)}}, {"idorg": 1})
#         else:
#             return self.orgrank_col.find({"type": isAcademic, "orgClusterText": {'$regex': re.compile(query)}},
#                                          {"idorg": 1})
#
#     def get_conf_with_type(self, type):
#         type = int(type)
#         confList = []
#         if type == 0:
#             cursor = self.ccf.find()
#             for item in cursor:
#                 confList.append(item)
#         else:
#             cursor = self.ccf.find({'TYPE': type})
#             for item in cursor:
#                 confList.append(item)
#         for c in confList:
#             del c["_id"]
#             del c["nameList"]
#             del c["idList"]
#         return confList
#
#     def get_bestpaper_vs_citation(self):
#         # result = {conf: [level, {year: [sorted_papers]}]}
#         result = {}
#         # n = 0
#         # try:
#         for conf in self.ccf_with_top3cited.find():
#             name = conf.get("SHORT_NAME")
#             # n += 1
#             # print("name {0:d}: {1:s}".format(n, name))
#             result[name] = [conf.get("LEVEL"), {}, 0]  # The last one is MAP
#             # venue_tmp = self.venue.find_one({"SHORT_NAME": name})
#             # id = int(venue_tmp.get("Id")[:-2])
#
#             ### update
#             # id = conf.get("oid")
#
#             # jconf_bestpapers = self.bestpaper.find({"jconf": id}, {"_id": 0})
#             for x in conf.get("top3_with_bestpapers"):
#                 year = x["year"]
#                 if year < 1996:
#                     continue
#                 tmp = []
#                 # i = 0
#                 for t in x["pubs_id"]:
#                     # i += 1
#                     # tmp2 = self.publication.find_one({"_id":t}, {"_id":0, "venue._id":0, "citation":0})
#                     tmp2 = self.publication.find_one({"_id": t['pid']}, \
#                                                      {"venue.raw": 1, "n_citation": 1, "title": 1, "authors.name": 1,
#                                                       "oid": 1, "year": 1, "url": 1})
#                     tmp2['_id'] = str(tmp2['_id'])
#                     tmp2['new_url'] = 'archive/' + tmp2['_id']
#                     # tmp2['isBest'] = False
#                     tmp2['isBest'] = t['isBest']
#                     tmp2['rank'] = t['rank']
#                     if "url" not in tmp2:
#                         tmp2["url"] = ""
#                     tmp.append(tmp2)
#                 result[name][1][year] = {"MAP": x['MAP'], "papers": tmp}
#             result[name][2] = conf.get("average_MAP")
#             """
#             for x in jconf_bestpapers:
#                 year = x.get("year")
#                 if year < 1996:
#                     continue
#                 pid = x.get("pid")
#                 #pub_tmp = self.publication.find_one({"oid":pid}, {"_id":0, "venue._id":0, "citation":0})
#                 pub_tmp = self.publication.find_one({"oid": pid, "n_citation": {"$exists": True}}, \
#                                                     {"venue.raw": 1, "n_citation": 1, "title": 1, "authors.name": 1,
#                                                      "oid": 1, "year": 1, "url": 1})
#                 if not pub_tmp:
#                     continue
#                 pub_tmp['_id'] = str(pub_tmp['_id'])
#                 pub_tmp['new_url'] = 'archive/' + pub_tmp['_id']
#                 #print("{0:s}, {1}".format(name,pub_tmp.get("_id")))
#                 #if (not pub_tmp) or ("n_citation" not in pub_tmp):
#                 #    continue
#                 exist = False
#                 if year not in result[name][1]:
#                     result[name][1][year] = []
#                 for t in result[name][1][year]:
#                     if t.get("oid") == pid:
#                         t["isBest"] = True
#                         exist = True
#                         break
#                 if not exist:
#                     pub_tmp["isBest"] = True
#                     pub_tmp["rank"] = x.get("rank")
#                     if "url" not in pub_tmp:
#                         pub_tmp["url"] = ""
#                     result[name][1][year].append(pub_tmp)
#
#             # the following part is to calculate MAP
#             all_MAP = 0
#             for year in result[name][1]:
#                 result[name][1][year] = sorted(result[name][1][year], key=lambda a: a["rank"])
#                 l = len(result[name][1][year])
#                 if l > 3:
#                     l = 3
#                 tmp = [0, 0, 0]
#                 for i in xrange(l):
#                     if result[name][1][year][i].get("isBest"):
#                         tmp[i] = 1
#                 MAP = 1 / 3.0 * (tmp[0] + (tmp[0] + tmp[1]) / 2.0 + (tmp[0] + tmp[1] + tmp[2]) / 3.0)
#                 all_MAP += MAP
#                 result[name][1][year] = {"MAP": MAP, "papers": result[name][1][year]}
#             result[name][2] = all_MAP / len(result[name][1])
#             # one_paper = original_pub + {"rank": int, "isBest": bool}
#             ######
#             # result = {conf: [level, {year: {"papers": [sorted_papers], "MAP": float}}, float]}
#             ######
#             ######
#             # one_paper = {'isBest': bool, 'title': str, 'url':str, 'authors': [{'name':author, 'org':str, 'url':str}], 'rank': int, 'n_citation':int}
#             ######
#             """
#
#             # except:
#             # print "......lala....."
#
#         print("get_bestpaper_vs_citation() over.")
#         return result
#
#     def get_valid_ccfconfs(self):
#         result = []
#         # pick out confs (exclude journals)
#         # raw_result = self.ccfjconflevel.find({"SHORT_NAME": {"$ne": ""}, "TYPE": 2},
#         # raw_result = self.ccfjconflevel.find({"SHORT_NAME": {"$ne": ""}},
#         raw_result = self.ccfjconflevel.find({},
#                                              {"_id": 0, "SHORT_NAME": 1, "LEVEL": 1})
#         for x in raw_result:
#             # pick out all confs which has bestpaper_records in our db
#             name = x.get("SHORT_NAME")
#             tmp = self.venue.find_one({'SHORT_NAME': name})
#             # tmp = self.venue.find_one({'name': name})
#             if (not tmp) or (type(tmp.get("Id")) != unicode):
#                 continue
#             jconf = int(tmp.get("Id")[:-2])
#             if not self.bestpaper.find_one({"jconf": jconf}):
#                 continue
#             x["oid"] = jconf
#             ######
#             # to do: top-cited-papers
#             ######
#             result.append(x)
#         print("get_valid_ccfconfs() over. Num of conf: {0:d}".format(len(result)))
#         return result
