# -*- coding: utf-8 -*-

import json

from flask import Blueprint, request, make_response
from flask_cors import cross_origin
from flask_uploads import UploadSet, IMAGES
from flask_jwt import jwt_required

upload = Blueprint('upload', __name__, url_prefix='/upload')

img_uploads = UploadSet("avatar", IMAGES)
pdf_uploads = UploadSet(name="pdf", extensions=('pdf'))


##
# @upload.route('/image/<imgid>/', methods=['PUT', 'POST'])
# @cross_origin(headers=['Content-Type', 'Authorization'])
# @jwt_required()
# def image_uploader(imgid):
#     reply_status = {}
#     if request.method == 'POST' and 'avatar' in request.files:
#         try:
#             avatar_name = img_uploads.save(request.files['avatar'])
#             reply_status["status"] = True
#             reply_status["url"] = "http://localhost/images" + imgid + "/" + avatar_name
#         except:
#             reply_status["status"] = False
#             reply_status["url"] = None
#     else:
#         reply_status["status"] = False
#         reply_status["message"] = "file not found"
#
#     response = make_response(json.dumps(reply_status))
#     response.headers['Content-Type'] = 'application/json'
#     return response
