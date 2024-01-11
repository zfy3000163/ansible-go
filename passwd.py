#-*- coding:utf-8 -*-
import os
import datetime
from passlib.hash import sha512_crypt
import getpass
import random
import string

#获取所有主机
f=os.popen("grep -E '^\[' /etc/ansible/hosts |grep -vE ':' |awk '{print $1}'")
host=list(f)

#显示主机
for index,element in enumerate(host):
    print(str(index)+':'+element)

def randpass(length=15):
    chars=string.ascii_letters+string.digits
    return ''.join([random.choice(chars) for i in range(length)])

#选择主机
choice=int(input('请选择主机,填写数字:'))
mechina=host[choice].strip().replace('[', '').replace(']', '')

#生成密码
mima=randpass()
#sha512mima=sha512_crypt.using(rounds=5000).hash(mima)
print('\nHOST IS:',mechina,'password:',mima,'\n')

#调用ansible修改密码
#os.system(("ansible-playbook -e user=engine -e name=root -e passwd=%s /mnt/work/ansible/ssh_key_and_change_pass.yaml") % (mima))
#result = os.popen(("ansible-playbook -e hosts=%s -e user=engine -e name=root -e passwd=%s /mnt/work/ansible/ssh_key_and_change_pass.yaml") % (mechina, mima))

result = os.popen(("./ansibleplaybook-go -L -i /etc/ansible/hosts -e hosts=%s -e user=dep -e name=root -e passwd=%s -p /mnt/work/ansible/ssh_key_and_change_pass.yaml") % (mechina, mima))
log = result.read()
print(log)
content = '\ndate: %s, passwd: %s, log:%s\n' % (datetime.datetime.now(), mima, log)
with open('/opt/change_passwd','a') as fd:
    fd.write(content)

