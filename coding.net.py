#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,sys
import ast,re

print "useage:python coding.net.py keyword"
host = "https://coding.net"

#############################################################关键字
keywords = sys.argv[1]
#keywords = 'jzb'
session = requests.session()
reheaders = {
    "Host":"coding.net",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding":"gzip, deflate",
    "Connection":"keep-alive",
}
#项目搜索API
searchurl = "https://coding.net/api/esearch/project?q=" + keywords + "&page=1"
#获取项目搜索结果
searchhtm = session.get(searchurl,headers=reheaders)

# if searchhtm.status_code != 200:
#     print "Requesting URL is with wrong response status."
#     exit()

# 将搜索结果转换成字典模式
resultdict = ast.literal_eval(searchhtm.text)  # .encode("utf-8")
# print resultdict
# 获取项目地址列表
data = resultdict.get('data')
inforlist = data.get('list')
# 匹配项目地址
for i in inforlist:
    project_path = i.get('project_path')
    print 'description= ' + i.get('description')
    # owner_user_home = i.get('owner_user_home')
    if project_path:
        # 匹配获取用户名及项目名。
        path = host + project_path #此项目的全路径
        print path
        reg1 = re.compile(r'/u/(.*?)/p', re.S)
        user = re.findall(reg1, project_path)
        reg2 = re.compile(r'/p/(.*?)$', re.S)
        projname = re.findall(reg2, project_path)
        # 获取单个项目提交历史。
        commithistoryurl = host + "/api/user/" + user[0] + "/project/" + projname[0] + "/git/commits/master/?page=1&pageSize=20"
        # print commithistoryurl
        commithistorydata = session.get(commithistoryurl, headers=reheaders)
        # print commithistorydata.text
        #获取历史提交ID
        reg3 = re.compile(r'commitId":"(.*?)",', re.S)
        historyCommitId = re.findall(reg3, commithistorydata.text)
        # print historyCommitId
        for j in historyCommitId:
            commitdiffurl = host + "/u/" + user[0] + "/p/" + projname[0] + "/git/commit/"+j+".diff"
            brourl = host + "/u/" + user[0] + "/p/" + projname[0] + "/git/commit/"+j+"?public=true"
            print "browerurl = "+brourl
            commitdetail = session.get(commitdiffurl, headers=reheaders)
            #print commitdetail.text
            #匹配多个关键字。 user login email jdbc password passwd pass pwd username.secretKey appid appkey smtp.100tal.com
            #(?:ip|host|sql|url|user|login|email|jdbc|password|passwd|pass|pwd|username|secretKey|appid|appkey|smtp.100tal.com)
            # 匹配任意一个。
            # 匹配内容很多行，要定位成单行。
            # 开头位置，任意内容，限定内容，任意内容，结束位置。
            reg4 = re.compile(r'^.*?(?:ip=|host|sql|url|user|login|email|jdbc|password|passwd|pass|pwd|username|secretKey|appid|appkey|smtp.100tal.com|http|ftp|ssh|mongo|redis|hadoop|rabbitmq).*?$', re.M)
            result = re.findall(reg4, commitdetail.text)
            regip = re.compile(r'^.*?(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).*?$', re.M)
            ip = re.findall(regip, commitdetail.text)
            print ip
            for r in result:
                print r.encode("utf-8")

        print '              '
        print '              '        
        print '####################################################################'


