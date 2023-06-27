import mysql.connector
import re
# 建立数据库连接
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="100221",
    database="scanner"
)

# 创建游标对象
cursor = cnx.cursor()

# 执行查询语句
select_query = "SELECT url,type FROM url_scanner"
cursor.execute(select_query)

# 获取查询结果
results = cursor.fetchall()

# 关闭游标对象和数据库连接
cursor.close()
cnx.close()

list_url = []
#暴力破解
bf = ['暴力破解']
#文件包含漏洞
include = ['文件包含漏洞']
#目录遍历漏洞
dum = ['目录遍历漏洞']
#文件上传和下载漏洞
file = ['文件上传和下载漏洞']
#SQL time blinds vulnerability
time_blinds = ['SQL time blinds vulnerability']
#SQL bool  blinds vulnerability
bool_blinds = ['SQL bool blinds vulnerability']
#SQL inject vulnerability
SQL_inject = ['SQL inject vulnerability']
#CSRF漏洞
CSRF = ['CSRF漏洞']
#PHP反序列化漏洞
PHP = ['PHP反序列化漏洞']
#XSS Href
Href = ['XSS Href']
#XSS POST Reflected
XSS_POST = ['XSS POST Reflected']
#XSS GET Reflected
XSS_GET = ['XSS GET Reflected']
#XSS Stored
XSS_Stored = ['XSS Stored']
#XSS JavaScript
XSS_JavaScript = ['XSS JavaScript']
#XSS DOM
XSS_DOM = ['XSS DOM']

for ret in results:
    pattern1 = r'暴力破解漏洞'
    if re.search(pattern1, ret[1]) is not None:
        print(ret)
        bf.append(ret[0])

    pattern2 = r'文件包含漏洞'
    if re.search(pattern2, ret[1]) is not None:
        include.append(ret[0])

    pattern3 = r'目录遍历漏洞'
    if re.search(pattern3, ret[1]) is not None:
        dum.append(ret[0])

    pattern4 = r'文件上传和下载漏洞'
    if re.search(pattern4, ret[1]) is not None:
        file.append(ret[0])

    pattern5 = r'SQL time blinds vulnerability'
    if re.search(pattern5, ret[1]) is not None:
        time_blinds.append(ret[0])

    pattern6 = r'SQL bool  blinds vulnerability'
    if re.search(pattern6, ret[1]) is not None:
        bool_blinds.append(ret[0])

    pattern7 = r'SQL inject vulnerability'
    if re.search(pattern7, ret[1]) is not None:
        SQL_inject.append(ret[0])

    pattern8 = r'CSRF漏洞'
    if re.search(pattern8, ret[1]) is not None:
        CSRF.append(ret[0])

    pattern9 = r'PHP反序列化漏洞'
    if re.search(pattern9, ret[1]) is not None:
        PHP.append(ret[0])

    pattern10 = r'XSS Href'
    if re.search(pattern10, ret[1]) is not None:
        Href.append(ret[0])

    pattern11 = r'XSS POST Reflected'
    if re.search(pattern11, ret[1]) is not None:
        XSS_POST.append(ret[0])

    pattern12 = r'XSS GET Reflected'
    if re.search(pattern12, ret[1]) is not None:
        XSS_GET.append(ret[0])

    pattern13 = r'XSS Stored'
    if re.search(pattern13, ret[1]) is not None:
        XSS_Stored.append(ret[0])

    pattern14 = r'XSS JavaScript'
    if re.search(pattern14, ret[1]) is not None:
        XSS_JavaScript.append(ret[0])

    pattern15 = r'XSS DOM'
    if re.search(pattern15, ret[1]) is not None:
        XSS_DOM.append(ret[0])

list_url.append(bf)
list_url.append(include)
list_url.append(dum)
list_url.append(file)
list_url.append(time_blinds)
list_url.append(bool_blinds)
list_url.append(SQL_inject)
list_url.append(CSRF)
list_url.append(PHP)
list_url.append(Href)
list_url.append(XSS_POST)
list_url.append(XSS_GET)
list_url.append(XSS_Stored)
list_url.append(XSS_JavaScript)
list_url.append(XSS_DOM)
print(list_url)
