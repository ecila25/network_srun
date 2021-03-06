import requests
import curlify
import time
import re
from encryption.srun_md5 import *
from encryption.srun_sha1 import *
from encryption.srun_base64 import *
from encryption.srun_xencode import *
header={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
init_url="http://192.168.167.14"
get_challenge_api="http://192.168.167.14/cgi-bin/get_challenge"

srun_portal_api="http://192.168.167.14/cgi-bin/srun_portal"
get_info_api="http://192.168.167.14/cgi-bin/rad_user_info?callback=jQuery1124030851040991675704_1656067282083&_=1656067282084"
n = '200'
type = '1'
ac_id='1'
enc = "srun_bx1"

def get_chksum():
	chkstr = token+username
	chkstr += token+hmd5
	chkstr += token+ac_id
	chkstr += token+ip
	chkstr += token+n
	chkstr += token+type
	chkstr += token+i
	return chkstr
def get_info():
	info_temp={
		"username":username,
		"password":password1,
		"ip":ip,
		"acid":ac_id,
		"enc_ver":enc
	}
	i=re.sub("'",'"',str(info_temp))
	i=re.sub(" ",'',i)
	return i
def init_getip():
	global ip
	init_res=requests.get(init_url,headers=header)
	print("初始化获取ip")
	ip=re.search('id="user_ip" value="(.*?)"',init_res.text).group(1)
	print("ip:"+ip)
def get_token():
	# print("获取token")
	global token
	get_challenge_params={
		"callback": "jQuery1124041017769561210393_"+str(int(time.time()*1000)),
		"username":username,
		"ip":ip,
		"_":int(time.time()*1000),
	}
	get_challenge_res=requests.get(get_challenge_api,params=get_challenge_params,headers=header)
	token=re.search('"challenge":"(.*?)"',get_challenge_res.text).group(1)
	print(get_challenge_res.text)
	print("token为:"+token)
def do_complex_work():
	global i,hmd5,chksum
	i=get_info()
	i="{SRBX1}"+get_base64(get_xencode(i,token))
	hmd5=get_md5(password1,token)
	chksum=get_sha1(get_chksum())
	print("所有加密工作已完成")
def login():
	srun_portal_params={
	'callback': 'jQuery1124041017769561210393_'+str(int(time.time()*1000)),
	'action':'login',
	'username':username,
	'password':'{MD5}'+hmd5,
	'ac_id':ac_id,
	'ip':ip,
	'chksum':chksum,
	'info':i,
	'n':n,
	'type':type,
	'os':'windows+10',
	'name':'windows',
	'double_stack':'0',
	'_':int(time.time()*1000)
	}
	# print(srun_portal_params)
	srun_portal_res=requests.get(srun_portal_api,params=srun_portal_params,headers=header)
	ret = curlify.to_curl(srun_portal_res.request,compressed=True)
	with open("login.sh",'w') as file:
		file.write(ret)
	print(srun_portal_res.text)


if __name__ == '__main__':
	global username
	global password1
	username="your username"	### 登录认证账号
	password1="your password" ### 登录认证密码
	init_getip()
	get_token()
	do_complex_work()
	login()
	res=requests.get(get_info_api,headers=header)
	print(res.text)