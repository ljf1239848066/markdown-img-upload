# -*- coding: utf-8
import os, re, subprocess
import configparser
from tempfile import NamedTemporaryFile

TARGET = 'alioss'
CONFIG_FILE = 'config.ini'

def notice(msg, title="notice"): 
    ''' notoce message in notification center'''
    os.system('osascript -e \'display notification "%s" with title "%s"\'' % (msg, title))

def picbed_name():
    if(TARGET=='qiniu'):
        return '七牛图床'
    elif(TARGET=='alioss'):
        return '阿里OSS对象存储'
    else:
        return '图床'

def read_config():
    ''' read congig from config.ini, return a five tuple'''
    if not os.path.exists(CONFIG_FILE):
        return
    cf = configparser.ConfigParser()
    cf.read(CONFIG_FILE)

    config_section = 'config'
    keys = ('ak', 'sk', 'url', 'bucket', 'prefix')
    try:
        res = list(map(lambda x: cf[config_section][x], keys))
    except configparser.NoOptionError:
        return
    
    if not all(map(lambda x: re.match(r'\w+', x), res)):
        return
    return dict(zip(keys, res))

def open_with_editor(filepath):
    ''' open file with apple's text editor'''
    os.system('open -b "com.apple.TextEdit" "./%s"' % CONFIG_FILE)

def generate_config_file():
    import textwrap
    name = picbed_name()
    config_file_init_content = '''\
    ; 详细设置见 https://github.com/tiann/markdown-img-upload
    [config]
    ak=%s的Access Key
    sk=%s的Secret Key
    url=%s地址
    bucket=%s空间名
    prefix=%s资源前缀名'''%(name,name,name,name,name)
    with open(CONFIG_FILE, 'w') as fp:
        fp.write(textwrap.dedent(config_file_init_content))

def try_compress_png(raw_img, need_compress):
    ''' use pngquant to compress:https://github.com/pornel/pngquant'''
    if not need_compress: return raw_img
    if not os.path.exists(raw_img.name): return raw_img
    tmp_file = NamedTemporaryFile()
    return tmp_file if not subprocess.call('pngquant/pngquant --force %s -o %s' \
        % (raw_img.name, tmp_file.name), shell=True) else raw_img
