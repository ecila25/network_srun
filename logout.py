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

def init_getip():
	global ip
	init_res=requests.get(init_url,headers=header)
	print("初始化获取ip")
	ip=re.search('id="user_ip" value="(.*?)"',init_res.text).group(1)
	print("ip:"+ip)

def logout():
	srun_portal_params={
	'callback': 'jQuery112409976310652735085_'+str(int(time.time()*1000)),
	'action':'logout',
	'ac_id':ac_id,
	'ip':ip,
	'username':username,
	'_':int(time.time()*1000)
	}
	srun_portal_res=requests.get(srun_portal_api,params=srun_portal_params,headers=header)
	ret = curlify.to_curl(srun_portal_res.request,compressed=True)
	with open("logout.sh",'w') as file:
		file.write(ret)
	print(srun_portal_res.text)
	
if __name__ == '__main__':
	global username
	global password1
	username="your username"	### 登录认证账号
	password1="your password" ### 登录认证密码
	init_getip()
	logout()
	res=requests.get(get_info_api,headers=header)
	print(res.text)