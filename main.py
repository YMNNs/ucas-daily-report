import argparse
from datetime import datetime

import pytz
import requests

import json2markdown

keys = ['date',
        'realname',
        'number',
        'jzdz',
        'zrzsdd',
        'sfzx',
        'dqszdd',
        'geo_api_infot',
        'szgj',
        'szgj_select_info[id]',
        'szgj_select_info[name]',
        'geo_api_info',
        'dqsfzzgfxdq',
        'zgfxljs',
        'tw',
        'sffrzz',
        'dqqk1',
        'dqqk1qt',
        'dqqk2',
        'dqqk2qt',
        'sfjshsjc',
        'dyzymjzqk',
        'dyzwjzyy',
        'dyzjzsj',
        'dezymjzqk',
        'dezwjzyy',
        'dezjzsj',
        'dszymjzqk',
        'dszwjzyy',
        'dszjzsj',
        'gtshryjkzk',
        'extinfo',
        'app_id']

# 从命令行获取参数

parser = argparse.ArgumentParser()

parser.add_argument('-u', '--username', help='SEP账号，一般为国科大电子邮件地址', default='')
parser.add_argument('-p', '--password', help='SEP密码', default='')
parser.add_argument('-n', '--server_chan_api_key', help='ServerChan的推送密钥', default='')

args = parser.parse_args()

login_url = 'https://app.ucas.ac.cn/uc/wap/login/check'
daily_info_url = 'https://app.ucas.ac.cn/ucasncov/api/default/daily?xgh=0&app_id=ucas'
submit_url = 'https://app.ucas.ac.cn/ucasncov/api/default/save'


def login(username, password):
    """
    登录
    :param username: SEP账号
    :param password: SEP密码
    :return: 当前会话，包含cookies
    """
    sess = requests.session()
    login_data = {
        'username': username,
        'password': password
    }
    res = sess.post(login_url, data=login_data)
    assert res.status_code == 200, '网络错误'
    status = res.json()
    assert status['e'] == 0, status['m']  # 登录失败
    return sess


def get_previous_info(sess):
    """
    获取上次填报信息
    :param sess: 当前会话
    :return: 上次填报信息
    """
    res = sess.get(daily_info_url)
    assert res.status_code == 200
    status = res.json()
    assert status['e'] == 0, '无法查询上次填报信息'
    return status['d']


def submit(sess, info):
    """
    提交填报信息
    :param sess: 当前会话
    :param info: 新的填报信息
    :return:
    """
    res = sess.post(submit_url, data=info)
    assert res.status_code == 200, '网络错误'
    status = res.json()
    assert status['e'] == 0, status['m']  # 填报失败


def send_message(_title, _content, api_key):
    """
    发送微信通知
    :param _title: 通知标题
    :param _content: 内容
    :param api_key: ServerChan的API_KEY
    :return:
    """
    requests.get(f'https://sctapi.ftqq.com/{api_key}.send?title={_title}&desp={_content}')


if __name__ == '__main__':
    try:
        # 获取登录会话
        session = login(args.username, args.password)

        # 获取上次填报信息
        previous_info = get_previous_info(session)

        # 构造新的填报信息
        new_info = {}

        # 过滤多余条目
        for key in keys:
            if key in previous_info.keys():
                new_info[key] = previous_info[key]
            else:
                new_info[key] = None

        # 将上次填报的日期修改为今天
        new_info['date'] = datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')

        # 添加app_id和其余信息
        new_info['app_id'] = 'ucas'
        new_info['szgj_select_info[id]'] = '0'

        # 提交
        submit(session, new_info)

        # 运行到这一行代表填报成功
        title = '填报成功'
        print(title)
        # 将今日填报信息转换为markdown
        content = json2markdown.Json2Markdown().json2markdown(new_info)
        if len(args.server_chan_api_key) > 0:
            send_message(title, content, args.server_chan_api_key)
        print('推送成功')
    except AssertionError as e:
        # 任何断言错误都会导致填报失败，向微信推送失败信息
        title = '填报失败'
        content = e
        if len(args.server_chan_api_key) > 0:
            send_message(title, content, args.server_chan_api_key)
        print(title,e)
    except Exception as e:
        # 微信推送失败或其他未知错误
        print(e)
