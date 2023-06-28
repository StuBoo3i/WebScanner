# -*- coding=utf8 -*-
# 导入Flask库
from flask import Flask
from flask import request
from flask import render_template
import plotly.graph_objs as go
from keras_preprocessing.sequence import pad_sequences
from threading import Thread
from keras.preprocessing.text import Tokenizer
import tensorflow as tf
import label_data
import flask
import json
from Web_Vulnerablility.main import scanweb,read_list_from_file
from static.Tools.SQL.SQL_op import SQL


app = Flask(__name__)

global graph
graph = tf.compat.v1.get_default_graph()


def prepare_url(url):
    urlz = label_data.main()

    samples = []
    labels = []
    for k, v in urlz.items():
        samples.append(k)
        labels.append(v)

    maxlen = 128
    max_words = 20000

    tokenizer = Tokenizer(num_words=max_words, char_level=True)
    tokenizer.fit_on_texts(samples)
    sequences = tokenizer.texts_to_sequences(url)
    '''
    创建一个Tokenizer对象，并使用样本数据samples对其进行训练，以便后续可以使用这个Tokenizer对象对文本数据进行编码和处理。训练过程中会构建词汇表和统计词频等信息，以供后续使用。
    '''
    word_index = tokenizer.word_index
    # print('Found %s unique tokens.' % len(word_index))

    url_prepped = pad_sequences(sequences, maxlen=maxlen)
    return url_prepped


# 写好的数据库连接函数，
# 传入的是table，数据表的名称，
# 返回值是数据表中所有的数据，以元祖的格式返回
# 模拟已知的漏洞列表（可以根据实际情况进行修改）
sql1 = SQL()
counter = sql1.selectSQL(sql1.cursor)[0]
vulnerabilities = {
    'XSS': '跨站脚本攻击（Cross-Site Scripting）',
    'SQLI': 'SQL 注入攻击（SQL Injection）',
    'RCE': '远程命令执行（Remote Code Execution）'
}

client_proxy = {
    "Internet Explorer 11": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Default": ""
}

scan_mode = {
    "全面扫描": 2,
    "快速扫描": 1,
    "SQL注入扫描": 3,
    "XSS扫描": 4,
    "暴力破解扫描": 5,
    "远程代码执行扫描": 6,
    "文件漏洞扫描": 7
}


shared_data = {

}


# 启动服务器后运行的第一个函数，显示对应的网页内容
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('login.html')


# 对登录的用户名和密码进行判断
@app.route('/login', methods=['POST'])
def login():
    # 需要从request对象读取表单内容：
    if request.form['username'] == 'student' and request.form['password'] == 'password':
        return render_template('scan.html')
    return render_template('student_index.html')


# 显示学生首页的函数，可以显示首页里的信息
@app.route('/student_index', methods=['GET'])
def student_index():
    return render_template('student_index.html')


# 显示教师首页的函数，可以显示首页里的信息
@app.route('/scan', methods=['GET', 'POST'])
def scan():
    message = ''
    if request.method == 'POST':
        url = request.form['url']
        scan_mode = request.form['scan_mode']
        speed = request.form['speed']
        proxy_name = request.form['username']
        proxy_password = request.form['password']
        proxy = request.form['proxy']
        thread_1 = Thread(target=subthread_scan, args=(url, scan_mode))
        thread_1.start()
        message = "扫描已开始，请勿重复提交请求！"
        # 返回响应，并将提示信息传递给模板
    return render_template('scan.html', message=message)


def subthread_scan(url, scan_mode):
    scanweb(url, scan_mode)  # 扫描完成后设置弹窗提示信息


@app.route('/result', methods=['GET', 'POST'])
def result():
    data = read_list_from_file()
    # print(data)
    return render_template('result.html', data=data)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    vulnerabilities_data = {
        '暴力破解漏洞': counter[0],
        '文件包含漏洞': counter[1],
        'SQL time blinds vulnerability': counter[4],
        'SQL bool blinds vulnerability': counter[5],
        'SQL inject vulnerability': counter[6],
        'PHP反序列化漏洞': counter[8],
        '目录遍历漏洞': counter[2],
        '文件上传和下载漏洞': counter[3],
        'XSS Href': counter[9],
        'XSS Stored': counter[12],
        'XSS JavaScript': counter[13],
        'XSS DOM' : counter[14],
        'CSRF漏洞' : counter[7],
        'XSS POST Reflected' : counter[10],
        'XSS GET Reflected' : counter[11]
    }

    target_data = [
        {'低危漏洞': counter[7]+counter[10]+counter[11],
         '中危漏洞': counter[2]+counter[3]+counter[9]+counter[12]+counter[13]+counter[14],
         '高危漏洞': counter[0]+counter[1]+counter[4]+counter[5]+counter[6]+counter[8]}
    ]
    # 生成饼状图1
    """
    高危漏洞列表： ['暴力破解漏洞', '文件包含漏洞', 'SQL time blinds vulnerability',
     'SQL bool blinds vulnerability', 'SQL inject vulnerability', 'PHP反序列化漏洞']
    中危漏洞列表： ['目录遍历漏洞', '文件上传和下载漏洞', 'XSS Href', 'XSS Stored', 'XSS JavaScript', 'XSS DOM']
    低危漏洞列表： ['CSRF漏洞', 'XSS POST Reflected', 'XSS GET Reflected']
    """

    labels1 = ['CSRF漏洞', 'XSS POST Reflected', 'XSS GET Reflected']
    values1 = [counter[7], counter[10], counter[11]]

    colors1 = ['#FFC300', '#3498DB', '#E74C3C']  # 自定义颜色

    pie_chart1 = go.Pie(labels=labels1, values=values1, textinfo='label', marker=dict(colors=colors1))

    pie_chart_layout1 = go.Layout(
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )

    pie_chart_fig1 = go.Figure(data=[pie_chart1], layout=pie_chart_layout1)
    pie_chart_fig1.update_traces(hole=0.2)

    pie_chart_div1 = pie_chart_fig1.to_html(full_html=False, default_height=250)

    # 生成饼状图2
    labels2 = ['目录遍历漏洞', '文件上传下载漏洞', 'XSS Href', 'XSS Stored', 'XSS JavaScript', 'XSS DOM']
    values2 = [counter[2], counter[3], counter[9], counter[12], counter[13], counter[14]]
    colors2 = ['#FFA500', '#800080', '#FFC0CB', '#A52A2A', '#00FFFF', '#808080']  # 自定义颜色

    pie_chart2 = go.Pie(labels=labels2, values=values2, textinfo='label', marker=dict(colors=colors2))

    pie_chart_layout2 = go.Layout(
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )

    pie_chart_fig2 = go.Figure(data=[pie_chart2], layout=pie_chart_layout2)
    pie_chart_fig2.update_traces(hole=0.2)

    pie_chart_div2 = pie_chart_fig2.to_html(full_html=False, default_height=250)

    # 生成饼状图3
    labels3 = ['暴力破解', '文件包含漏洞', 'SQL time blinds',
               'SQL bool blinds', 'SQL inject vul', 'PHP反序列化']
    values3 = [counter[0], counter[1], counter[4], counter[5], counter[6], counter[8]]

    colors3 = ['#FFA500', '#800080', '#FFC0CB', '#A52A2A', '#00FFFF', '#808080']  # 自定义颜色

    pie_chart3 = go.Pie(labels=labels3, values=values3, textinfo='label', marker=dict(colors=colors3))

    pie_chart_layout3 = go.Layout(
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )

    pie_chart_fig3 = go.Figure(data=[pie_chart3], layout=pie_chart_layout3)
    pie_chart_fig3.update_traces(hole=0.2)

    pie_chart_div3 = pie_chart_fig3.to_html(full_html=False, default_height=250)

    return render_template('dashboard.html', pie_chart1=pie_chart_div1, pie_chart2=pie_chart_div2,
                           pie_chart3=pie_chart_div3, target_data=target_data,
                           vulnerabilities_data=vulnerabilities_data)


@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')


@app.route('/fish', methods=['GET', 'POST'])
def fish():
    if request.method == "POST":
        message = []
        if 'url' in request.form:
            # 处理URL表单的逻辑
            url = request.form['url']
            # 执行URL表单的处理操作
            print(url)
            ans = url_detect(url)
            if ans == ['bad']:
                result = "Detection Result for URL: {}".format("是钓鱼网站")
            else:
                result = "Detection Result for URL: {}".format("不是钓鱼网站")
            return jsonify({'urlOrImage': url, 'result': result})
            print(ans)
            data = {
                'url': url,
                'info': ans
            }
            message.append(data)
        if 'image' in request.form:


            image = request.files['image']

            image.save('uploads/' + image.filename)
            classification = image_detect("uploads/"+image.filename)
            result = "Detection Result for Image: {}".format(classification)
            return jsonify({'urlOrImage': 'Uploaded Image', 'result': result})
            print(classification)
            data = {
                'url': url,
                'info': classification
            }
            message.append(data)
        return render_template('fish.html',message = message)
    return render_template('fish.html')


# 主函数
if __name__ == '__main__':
    # app.debug = True
    app.run()
