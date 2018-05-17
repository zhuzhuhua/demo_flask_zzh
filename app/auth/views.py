# -*- coding:utf-8 -*-

__author__ = 'eric'

import ldap

from flask import request, make_response, session, jsonify, abort
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, \
    create_access_token, jwt_refresh_token_required, \
    create_refresh_token, get_jwt_identity, get_jwt_claims, get_raw_jwt

from app.models import User
from app.auth import auth
from app import logger

jwt = JWTManager()
blacklist = set()


@auth.route('/login', methods=['POST'])
def login():
    """
    @api {post} /api/auth/login 用户登录
    @apiVersion 1.0.0
    @apiName login
    @apiGroup Auth
    @apiParam {String}  username      (必须)    LDAP用户
    @apiParam {String}  password    (必须)    LDAP密码
    @apiParam {String}  captcha    (必须)    验证码
    @apiParamExample {json} Request-Example:
        {
            "username": "test",
            "password": "123456",
            "captcha": "1234"
        }

    @apiSuccessExample {json} Success-Response:
        {
            "code": 0,
            "data": {
                "access_token": "tWR5m9eeoePRQ0JgFeU21eeR7kWLF8tftrNxTXC8wxE",
                "refresh_token": "AD3Ne3wCmmWGbA5trRn9Vt8P16baB1cDn64v_rgmeoM"
            },
            "msg": "用户登录成功."
        }

    @apiErrorExample {json} Error-Response:
        {
            "code":1,
            "msg":"用户密码错误,"
        }

    """

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    captcha = request.json.get('captcha', None)

    if not User.verify_captcha(session.get('captcha'), captcha):
        return jsonify({
            'msg': '验证码错误!',
            'code': 2,
        }), 200

    try:
        data = User.search('uid', username)
        if not User.try_login(data[0], password):
            raise ldap.INVALID_CREDENTIALS
    except Exception as e:
        logger.error(e)
        return jsonify({
            'code': 1,
            'msg': '用户密码错误. %s' % e.message
        })

    try:
        user = User.query.filter(User.username == username).first() or User.query.filter(User.email == username).first()
        if not user:
            email = data[1]['mail'][0]
            if not email:
                raise ValueError('User: %s ,未配置邮箱.' % username)
            user = User.create_user({
                'username': username,
                'name': data[1]['displayName'][0] if data[1].has_key('displayName') else None,
                'email': email
            })
            logger.info('New User %s' % username)
        user.ping()
        db.session.add(user)
        db.session.commit()
        logger.info('User: %s login success.' % username)
    except Exception as e:
        logger.error(e)
        return jsonify({
            'code': 1,
            'msg': '登录错误, 请联系管理员, %s' % e.message
        })

    return jsonify({
        'msg': '用户登录成功.',
        'code': 0,
        'data': user.generate_token(1)
    })


@jwt.expired_token_loader
def my_expired_token_callback():
    return jsonify({
        'code': 401,
        'msg': '凭据过期.'
    })


@jwt.unauthorized_loader
def unauthorized_token_callback(msg):
    return jsonify({
        'code': 401,
        'msg': msg,
    }), 200


@jwt.invalid_token_loader
def invalid_token_callback(msg):
    return jsonify({
        'code': 401,
        'msg': msg,
    }), 200


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'code': 401,
        'msg': '无效凭据.',
    }), 200


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@auth.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """
    @api {post} /api/auth/refresh 刷新token
    @apiVersion 1.0.0
    @apiName refresh
    @apiGroup Auth
    @apiParamExample {json} Request-Example:
        Headers:{
            Authorization:"refresh_token"
            Content-Type:"application/json"
        }

    @apiSuccessExample {json} Success-Response:
        {
            'code': 0,
            'msg': '获取Token成功.',
            'data': {
                'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ'
            }
        }

    @apiErrorExample {json} Error-Response:
        {
            "code":1,
            "msg":"获取Token失败,"
        }

    """
    uid = get_jwt_identity()
    return jsonify({
        'code': 0,
        'msg': '获取Token成功.',
        'data': {
            'access_token': create_access_token(identity=User.query.get_or_404(uid))
        }
    })


@jwt.user_identity_loader
def user_identity_lookup(identity):
    return identity.id


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'info': identity.to_json(),
    }


@auth.route('/protected', methods=['GET'])
@jwt_required
def protected():
    uid = get_jwt_identity()
    claims = get_jwt_claims()
    return jsonify({'uid': uid, 'claims': claims}), 200


@auth.route('/logout', methods=['POST'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({
        'code': 0,
        "msg": "Successfully logged out"
    }), 200


@auth.route('/logout2', methods=['POST'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({
        'code': 0,
        "msg": "Successfully logged out"
    }), 200


@auth.route('/current_user', methods=['GET'])
@jwt_required
def current_user():
    """
        @api {post} /api/auth/current_user 获取当前用户信息
        @apiVersion 1.0.0
        @apiName current_user
        @apiGroup Auth


        @apiSuccessExample {json} Success-Response:
            {
                "code": 0,
                "data": {
                    "create_time": "2018-01-16 13:31:42",
                    "email": "xxx@jiagouyun.com",
                    "id": 2,
                    "is_admin": true,
                    "is_locked": null,
                    "last_seen": "2018-03-20 10:55:51",
                    "location": null,
                    "mobile": null,
                    "name": "zyadmin",
                    "username": "zyops"
                },
                "msg": "获取用户信息."
            }

        @apiErrorExample {json} Error-Response:
            {
                 "code":1,
                 "msg": "获取失败."
            }

        """
    user = get_jwt_identity()
    if not current_user:
        abort(401)

    user = User.query.get_or_404(user)
    return jsonify({
        'msg': '获取用户信息.',
        'code': 0,
        'data': user.to_json(),
    }), 200


@auth.route('/menus', methods=['GET'])
@jwt_required
def current_user_menus():
    """
        @api {post} /api/auth//menus 获取菜单
        @apiVersion 1.0.0
        @apiName current_user
        @apiGroup Auth


        @apiSuccessExample {json} Success-Response:
            {
                "code": 0,
                "data": {
                    "customer": [
                        {
                            "category": "customer",
                            "children": [
                                {
                                    "category": "customer",
                                    "create_time": "Wed, 17 Jan 2018 15:06:28 GMT",
                                    "id": 10,
                                    "is_show": true,
                                    "name": "项目信息",
                                    "parent_id": 14,
                                    "position": null,
                                    "remarks": "",
                                    "url": "/customer/information/project"
                                }
                            ],
                            "create_time": "Wed, 17 Jan 2018 16:05:45 GMT",
                            "id": 14,
                            "is_show": true,
                            "name": "客户信息",
                            "parent_id": null,
                            "position": 1,
                            "remarks": "",
                            "url": "/information"
                        },
                        ...
                    }
            }

        @apiErrorExample {json} Error-Response:
            {
                 "code":1,
                 "msg": "获取失败"
            }

        """
    user = User.query.get_or_404(get_jwt_identity())
    menus = {}
    for category in ['top', 'customer', 'hosts']:
        menus[category] = user.get_userMenus(user.id, category)
    return jsonify({
        'code': 0,
        'msg': '获取成功',
        'data': menus
    })


@auth.route('/permissions', methods=['GET'])
@jwt_required
def current_user_permissions():
    user = get_jwt_identity()
    if not user:
        abort(401)
    user = User.query.get_or_404(current_user)


@auth.route('/captcha')
def generate_captcha():
    """
    @api {get} /api/auth/captcha 验证码
    @apiVersion 1.0.0
    @apiName captcha
    @apiGroup Auth
    """
    captcha = User.generate_captcha()
    session['captcha'] = captcha[1]
    response = make_response(captcha[0])
    response.headers['Content-Type'] = 'image/jpeg'
    return response
