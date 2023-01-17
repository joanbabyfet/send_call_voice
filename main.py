import os
import pandas as pd
import configparser
from twilio.rest import Client
import utils

# 配置文件
config_file = 'config.ini'

# 发送短信
def send_sms(item):
    # 这里要转字符串, 否则文本为数字会报错, 空值会返回nan也要处理
    phone   = '' if pd.isnull(item['phone']) else '+' + str(item['phone']) # 联系人手机号, 不加+也能收到, 格式 85586207239
    name    = '' if pd.isnull(item['name']) else str(item['name'])   # 联系人姓名
    content = '' if pd.isnull(item['content']) else str(item['content']) # 短信内容
    
    try:
        conf = configparser.ConfigParser()
        conf.read(config_file, encoding='utf-8') # 这里要加utf-8, 否则会报错, 默认gbk
        config_section  = 'twilio_config'
        twilio_number   = conf.get(config_section, 'twilio_number') # 申请号码
        account_sid     = conf.get(config_section, 'account_sid')
        auth_token      = conf.get(config_section, 'auth_token')
        
        # 短信内容支持中文
        client = Client(account_sid, auth_token) # 实例化
        message = client.messages.create(body = content, from_ = twilio_number, to = phone)
        if message.sid != '':
            msg = '【短信】 %s %s %s 发送成功 %s' % (name, phone, content, message.sid)
        else:
            msg = '【短信】 %s %s %s 发送失败' % (name, phone, content)
        utils.logger(msg) # 写入日志
        print(msg)
    except Exception as e:
        msg = '【短信】 %s 发送失败' % e
        utils.logger(msg) # 写入日志
        print(msg)

# 发送电话提醒
def send_voice(item):
    # 这里要转字符串, 否则文本为数字会报错, 空值会返回nan也要处理
    phone   = '' if pd.isnull(item['phone']) else '+' + str(item['phone']) # 联系人手机号, 不加+也能收到, 格式 85586207239
    name    = '' if pd.isnull(item['name']) else str(item['name'])   # 联系人姓名
    
    try:
        conf = configparser.ConfigParser()
        conf.read(config_file, encoding='utf-8') # 这里要加utf-8, 否则会报错, 默认gbk
        config_section  = 'twilio_config'
        twilio_number   = conf.get(config_section, 'twilio_number') # 申请号码
        account_sid     = conf.get(config_section, 'account_sid')
        auth_token      = conf.get(config_section, 'auth_token')
        voice_url       = conf.get(config_section, 'voice_url')
        
        client = Client(account_sid, auth_token) # 实例化
        call = client.calls.create(url = voice_url, from_ = twilio_number, to = phone)
        if call.sid != '':
            msg = '【电话】 %s %s 发送成功 %s' % (name, phone, call.sid)
        else:
            msg = '【电话】 %s %s 发送失败' % (name, phone)
        utils.logger(msg) # 写入日志
        print(msg)
    except Exception as e:
        msg = '【电话】 %s 发送失败' % e
        utils.logger(msg) # 写入日志
        print(msg)

def main():
    if not os.path.exists(os.path.join(os.getcwd(), config_file)): # 检测配置文件是否存在
        print('%s 配置文件不存在' % config_file)
    else:
        df = pd.read_csv('list.csv', encoding='utf-8')
        method = input('请选择通知方式 1=发送短信 2=电话提醒:')
        if method == '1':
            df.apply(send_sms, axis=1) # apply添加send_sms函数, 且数据逐行加入
        else:
            df.apply(send_voice, axis=1)

if __name__ == '__main__': # 主入口
    main()