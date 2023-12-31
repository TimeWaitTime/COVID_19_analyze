from random import randrange
import tkinter as tk
from tkinter import messagebox

from flask.json import jsonify
from flask import Flask, render_template, redirect, url_for
from flask import request

import pandas as pd

from pyecharts import options as opts
from pyecharts.charts import Line

from myScripts.mapchina import render_mapcountChina
from myScripts.mapworld import render_mapcountWorld
from myScripts.lineCountry import render_lines
from myScripts.jiebafenci import render_wordcloud
from myScripts.weiboAnalyse import weiboWordcloud

n = "dataSets/countrydata.csv"
data = pd.read_csv(n)
date_list = list(data[data['countryName'] == '中国']['dateId'])
countrylist = list(data[data['dateId'] == 20200412]['countryName'])
countrylist = ['中国']+countrylist
#print(date_list)
#print(countrylist)

app = Flask(__name__, static_folder="templates")


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "123456":
        return redirect(url_for('index'))
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo('提示', '账号或密码错错误！', parent=None)
        return redirect(url_for('init'))


@app.route("/")
def init():
    return render_template("login.html")

@app.route("/a")
def a():
    return render_template("a.html", cates = countrylist)
@app.route("/Epidemic map")
def Epidemicmap():
    return render_template("Epidemic map.html", cates = countrylist)
@app.route("/Epidemic data curve")
def Epidemicdatacurve():
    return render_template("Epidemic data curve.html", cates = countrylist)

@app.route("/calendar chart")
def calendarchart():
    return render_template("calendar chart.html", cates = countrylist)

@app.route("/weibocloud")
def weibocloud():
    return render_template("weibocloud.html", cates = countrylist)

@app.route("/worldcloud")
def worldcloud():
    return render_template("worldcloud.html", cates = countrylist)
@app.route("/weiboemo")
def weiboemo():
    return render_template("weiboemo.html", cates = countrylist)
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/b")
def b():
    return render_template("b.html")

@app.route("/TFIDF")
def TFIDF():
    return render_template("TFIDF.html")


@app.route("/julei")
def julei():
    return render_template("julei.html")


@app.route("/document")
def document():
    return render_template("README.html")

@app.route("/nlp")
def nlpNotebook():
    return render_template("NLP.html")

@app.route("/analyse")
def anaNotebook():
    return render_template("analyse.html")

@app.route("/worldmap",methods=['POST', 'GET'])
def get_world_map():
    if request.method == 'GET':
        maptype = int(request.args.get('type', ''))
        i = int(request.args.get('index', ''))
        print(maptype)
        print(i)
        return render_mapcountWorld(date_list[int(i)],maptype).dump_options_with_quotes()


@app.route("/chinamap",methods=['POST', 'GET'])
def get_china_map():
    if request.method == 'GET':
        maptype = int(request.args.get('type', ''))
        i = int(request.args.get('index', ''))
        print(maptype)
        print(i)
        return render_mapcountChina(date_list[int(i)],maptype).dump_options_with_quotes()

@app.route("/lines")
def get_line_chart():
    return render_lines('中国').dump_options_with_quotes()

@app.route("/wordcloud",methods=['POST', 'GET'])
def get_word_chart():
    if request.method == 'GET':
        i = request.args.get('value', '')
        if not i:
            i = 0
        print(i)
        return render_wordcloud(i).dump_options_with_quotes()

@app.route("/weiboCloud",methods=['POST', 'GET'])
def get_weibo_chart():
    if request.method == 'GET':
        i = request.args.get('value', '')
        if not i:
            i = 0
        print(i)
        return weiboWordcloud(i).dump_options_with_quotes()

@app.route('/changecountry',methods=['POST', 'GET'])
def changeCountry():
    if request.method == 'GET':
        selectCountry = request.args.get('value', '')
        print(selectCountry)
        return render_lines(selectCountry).dump_options_with_quotes()
        
if __name__ == "__main__":
    app.run()