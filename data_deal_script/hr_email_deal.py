import pymysql
import re
import codecs
#连接配置信息
config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'spider',
          'password':'123',
          'db':'spider',
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
          }

conn = pymysql.connect(**config)

cursor = conn.cursor()


sql = """
    SELECT * FROM spider.yjs_other;
"""

cursor.execute(sql)

data = cursor.fetchall()

# 声明稍后要更新的数据
update_sql_part = ''
# 正则匹配邮箱
p = re.compile(r"[a-zA-Z0-9]+[\_]*[a-zA-Z0-9]+[@|#][a-zA-Z0-9]+\.[a-zA-Z0-9]+[[\.]*[a-zA-Z0-9]*]*")
ids_list = []
for row in data:

    hr_email = p.findall(row['content'])
    hr_email = list(set(hr_email))
    hr_email = (',').join(hr_email).replace('#','@')
    if hr_email:
        email_tuple = ()
        email_tuple = (row['id'],hr_email)
        ids_list.append(str(row['id']))
        update_sql_part += "when %d then '%s' \r\n" % email_tuple

ids = (",").join(ids_list)
update_sql = "update yjs_other SET hr_email = case id " + update_sql_part + " END where id in (" + ids + ")"
with codecs.open('update.sql','w','utf-8') as f:
    f.write(update_sql)
res = cursor.execute(update_sql)
cursor.close()
conn.close()
print(res)