import getManhua
import getXiaoshuo
import sqlite3
import os


if __name__ == '__main__':
    book_root_path = "./XiaoShuo/"

    manhuadatas=[]
    manhuadata1=getManhua.getRescult('https://ac.qq.com/Comic/comicInfo/id/649980', 2)
    manhuadata2=getManhua.getRescult('https://ac.qq.com/Comic/comicInfo/id/650030', 2)
    manhuadatas.append(manhuadata1)
    manhuadatas.append(manhuadata2)

    xiaoshuodatas=[]
    xiaoshuodata1=getXiaoshuo.getRescult('https://www.xbiquge.la/10/10489/', 10)
    xiaoshuodata2=getXiaoshuo.getRescult('https://www.ibiquge.la/98/98990/', 10)
    xiaoshuodata3=getXiaoshuo.getRescult('https://www.ibiquge.la/96/96419/', 10)
    xiaoshuodata4=getXiaoshuo.getRescult('https://www.ibiquge.la/7/7552/', 10)
    xiaoshuodata5=getXiaoshuo.getRescult('https://www.ibiquge.la/47/47167/', 10)

    xiaoshuodatas.append(xiaoshuodata1)
    xiaoshuodatas.append(xiaoshuodata2)
    xiaoshuodatas.append(xiaoshuodata3)
    xiaoshuodatas.append(xiaoshuodata4)
    xiaoshuodatas.append(xiaoshuodata5)

    file = open(os.getcwd() + "/" +'test.db', 'w')
    file.close()
    conn = sqlite3.connect(os.path.join(os.getcwd(), "test.db"))
    cur = conn.cursor()


    # 建表的sql语句
    sql_text_1 = '''CREATE TABLE 漫画
               (漫画名称 TEXT,
                作者名称 TEXT,
                话名称 TEXT,
                话路径 TEXT,
                话图片数 TEXT);'''
    cur.execute(sql_text_1)

    sql_text_2 = '''CREATE TABLE 小说
               (小说名称 TEXT,
                作者名称 TEXT,
                总字数 TEXT,
                小说文件路径 TEXT,
                小说文件名称 TEXT,
                占用空间 TEXT);'''
    cur.execute(sql_text_2)

    for manhuadata in manhuadatas:
        datatuple=[]
        for data in manhuadata:
            datatuple.append(tuple(data))
        # print(datatuple)
        cur.executemany('INSERT INTO 漫画 VALUES (?,?,?,?,?)', datatuple)

    for xiaoshuodata in xiaoshuodatas:
        datatuple=[]
        datatuple.append(tuple(xiaoshuodata))
        #print(datatuple)
        cur.executemany('INSERT INTO 小说 VALUES (?,?,?,?,?,?)', datatuple)

    conn.commit()
    conn.close()

