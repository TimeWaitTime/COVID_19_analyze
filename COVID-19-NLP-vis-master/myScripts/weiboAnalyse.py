from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
from pyecharts.globals import CurrentConfig, NotebookType
import pandas as pd
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
import mysql.connector

import sys

# 添加模块所在的绝对路径
module_path = 'C:/Users/lenovo/Desktop/COVID-19/COVID-19-NLP-vis-master/myScripts'
sys.path.append(module_path)
from myScripts.weiboWordData import date_data
def generateData():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="hw8"
    )
    print("Opened database successfully" )

    cur = conn.cursor()
    results = []
    for d in range(1,32):
        m = 1
        query = """
        with weibo_d as(
            select * from weibo where day = %d and month = %d
        )
        select k0.keyword, k0.c+k1.c+k2.c+k3.c as c from 
        (select keyword0 keyword,count(*) c from weibo_d group by keyword0) k0,
        (select keyword1 keyword,count(*) c from weibo_d group by keyword1) k1,
        (select keyword2 keyword,count(*) c from weibo_d group by keyword2) k2,
        (select keyword3 keyword,count(*) c from weibo_d group by keyword3) k3
        where k0.keyword = k1.keyword and k2.keyword = k1.keyword and k2.keyword = k3.keyword and k1.keyword != '##'
        order by c desc limit 50;
        """%(d,m)
        cur.execute(query)
        rows = cur.fetchall()
        results.append(((m,d),rows))
        print(rows)


    for d in range(1,19):
        m = 2
        query = """
        with weibo_d as(
            select * from weibo where day = %d and month = %d
        )
        select k0.keyword, k0.c+k1.c+k2.c+k3.c as c from 
        (select keyword0 keyword,count(*) c from weibo_d group by keyword0) k0,
        (select keyword1 keyword,count(*) c from weibo_d group by keyword1) k1,
        (select keyword2 keyword,count(*) c from weibo_d group by keyword2) k2,
        (select keyword3 keyword,count(*) c from weibo_d group by keyword3) k3
        where k0.keyword = k1.keyword and k2.keyword = k1.keyword and k2.keyword = k3.keyword and k1.keyword != '##'
        order by c desc limit 50;
        """%(d,m)
        cur.execute(query)
        rows = cur.fetchall()
        results.append(((m,d),rows))
        print(rows)
    
    return results


def generateSentimentsline():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="hw8"
    )
    print("Opened database successfully")

    cur = conn.cursor()
    query = "select concat(month, '-', day) as time, avg(sentiments) from weibo group by day, month order by month, day;"
    cur.execute(query)
    rows = cur.fetchall()

    date_list = []
    s_list = []
    for row in rows:
        date_list.append(row[0])
        s_list.append(row[1])

    line = (
        Line()
        .add_xaxis(date_list)
        .add_yaxis(
            series_name='sentiments',
            y_axis=s_list,
            is_smooth=True,
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"), opts.MarkPointItem(type_="min")])
        )
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False)
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
            yaxis_opts=opts.AxisOpts(name='sentiments', min_=0),
            title_opts=opts.TitleOpts(title='微博情感分析每日平均值')
        )
    )

    line.render("微博情感分析每日平均值.html")


# dateId: 0-50
def weiboWordcloud(dateId):

    words = date_data[int(dateId)][1]
    date = date_data[int(dateId)][0]
    c = (
        WordCloud()
        .add("", words, word_size_range=[20, 100], shape=SymbolType.ROUND_RECT)
        .set_global_opts(title_opts=opts.TitleOpts(title='全国新型冠状病毒疫情微博每日主题词词云图 '+str(date)))
    )
    return c

def weiboidf():
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.font_manager import FontProperties
    keywords_df = pd.read_csv('C:/Users/lenovo/Desktop/COVID-19/COVID-19-NLP-vis-master/dataSets/TF_IDF关键词前50.csv')
    keywords = keywords_df[['词语', '重要性']].values.tolist()
    ss = pd.DataFrame(keywords, columns=['词语', '重要性'])

    plt.figure(figsize=(10,6))
    plt.title('TF-IDF Ranking')
    fig = plt.axes()
    plt.barh(range(len(ss.重要性[:25][::-1])),ss.重要性[:25][::-1])
    fig.set_yticks(np.arange(len(ss.重要性[:25][::-1])))
    font_prop = FontProperties(fname='C:/Windows/Fonts/simsun.ttc')
    # 设置y轴刻度标签的字体属性
    fig.set_yticklabels(ss.词语[:25][::-1], fontproperties=font_prop)
    fig.set_xlabel('Importance')
    plt.show()

if __name__ == "__main__":
    #weiboidf()
    #generateSentimentsline()
    weiboWordcloud(20)
    # results = generateData()
    # with open("weiboWordData.py",'w',encoding='utf-8') as f:
    #     f.write("date_data="+str(results))
    #     f.close()
