# -*- coding: UTF-8 -*-
from flask import request, jsonify, render_template
from app.models import *
from app.auth import auth
from app.models.users import User



@auth.route('/apidemo', methods=['GET', 'POST'])
def apidemo():
    """一个返回JSON数据接口的设计示例"""
    if request.method == 'GET':
        result = User.query.filter().all()
        # return jsonify({'data': [{
        #     "id": i.id,
        #     "UserCode": i.UserCode,
        #     "Password": i.Password
        # } for i in result]}, {"count": len(result)})
        return jsonify([i.to_json() for i in result])
    else:
        jsonResponse = dict(errCode="1", errMsg="操作成功！")
        response = jsonify(jsonResponse)
        return response
