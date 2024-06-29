import pymysql
import xlwt

def export_to_excel(worksheet, cursor, table):
    """
    将MySQL一个数据表导出到excel文件的一个表的函数
    :param    worksheet:  准备写入的excel表
    :param    cursor:     源数据的数据库游标
    :param    table       源数据的数据表
    :return:  Nove.
    """
    # 首先向excel表中写入数据表的字段
    column_count = cursor.execute("desc %s"%table)
    for i in range(column_count):
       temptuple = cursor.fetchone()
       worksheet.write(0, i, temptuple[0])

    # 向构建好字段的excel表写入所有的数据记录
    row_count = cursor.execute("select * from %s"%table)
    for i in range(row_count):
        temptuple = cursor.fetchone()
        for j in range(column_count):
            worksheet.write(i + 1, j, temptuple[j])

workbook = xlwt.Workbook()
connect = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='xxxxx',
        db='forum'
    )
cursor = connect.cursor()
cursor.execute("SHOW TABLES;")
c=cursor.fetchall()
titles=[title for li in c for title in li]
for title in titles:
    worksheet = workbook.add_sheet(title)
    export_to_excel(worksheet, cursor, title)

cursor.close()
connect.close()

workbook.save("貼圖寫真.xls")