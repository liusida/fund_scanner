from wechatpy import WeChatClient
app_id = 'wxdf080559f2573b5c'
secret = ''
userid = {}
userid['liusida'] = 'oLnoquClb-5J-TOTNGBDnotESACU'
template_id = 'aSYZUJ5Fcrg7GBVXvs1cuzJXdSYgxc5mn8hEfaNziD0' #报告生成通知

template_data = {
    'first':{'value':'', 'color':'#000099'},
    'keyword1': {'value': '', 'color': ''},
    'keyword2': {'value': '', 'color': ''},
    'keyword3': {'value': '', 'color': ''},
    'remark': {'value': '', 'color': ''}
}

with open('secret.pwd', 'r') as f:
	secret = f.read()

def send(msg='默认消息'):
    global template_data
    template_data['first']['value'] = msg
    client = WeChatClient(app_id, secret)
    client.message.send_template(userid['liusida'], template_id, template_data)
