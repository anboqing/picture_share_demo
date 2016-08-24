# encoding=utf-8
import os

from qiniu import Auth, put_data
from picture_share import app



def qiniu_upload_file(source_file,save_file_name):
    '''
    :param source_path:
        要上传文件的本地路径
    :param save_file_name:
        上传到七牛后保存的文件名
    :return:
    '''
    # 需要填写你的 Access Key 和 Secret Key
    access_key = app.config['AK']
    secret_key = app.config['SK']
    domain_prefix = app.config['QINIU_DOMAIN']
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = app.config['QINIU_BUCKET_NAME']
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name,save_file_name)
    ret, info = put_data(token,save_file_name,source_file.stream)
    if info.status_code==200:
        return domain_prefix+save_file_name
    return None
