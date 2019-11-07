# -*- coding: utf-8 -*-

import os
import oss2
from qiniu import Auth, put_file
import util

config = util.read_config()

def upload_qiniu(path, upload_name):
    ''' upload file to qiniu'''
    q = Auth(config['ak'], config['sk'])
    key = '%s/%s' % (config['prefix'], upload_name) # upload to qiniu's markdown dir

    token = q.upload_token(config['bucket'], key)
    ret, info = put_file(token, key, path, check_crc=True)
    return ret != None and ret['key'] == key

def upload_alioss(path, upload_name):
    ''' upload file to ali oss'''
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth(config['ak'], config['sk'])
    key = '%s/%s' % (config['prefix'], upload_name) # upload to alioss's markdown dir
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    url = config['url'].replace(config['bucket']+'.','')
    bucket = oss2.Bucket(auth, url, config['bucket'])
    ret = bucket.put_object_from_file(key, path)
    return ret != None and ret.status == 200

def upload_img(path, upload_name):
    if(util.TARGET=='qiniu'):
        return upload_qiniu(path, upload_qiniu)
    elif(util.TARGET=='alioss'):
        return upload_alioss(path, upload_name)