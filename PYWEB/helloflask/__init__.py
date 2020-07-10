from flask import Flask, g, make_response,Response,request
from datetime import date, datetime

#app optiton
app = Flask(__name__)
app.debug = True

#local.com 으로 이제 접근가능하게 설정함
app.config["SERVER_NAME"] ='local.com:5000'  #os host에서 해당도메인으로  이렇게 설정을 미리 해놧음 127.0.0.1

#flask.g 는 Application Context에 값을 가짐

#Application Context :모든 유저가 접근
#Session Context : 유저마다 접근가능한 영역 (암호화 되어 저장됨)

#event handler
# @app.before_request  #route 요청전에 항상 실행되는 것들
# def before_request():
#     print("before_request!!!")
#     g.str = "한글"  

# localhost:5000/rp?q=123 
# request.args.get('q')로 123을 불러옴
# GET방식으로 request시

#request 처리 용 함수
def ymd(fmt):
	def trans(date_str):
			return datetime.strptime(date_str,fmt) # date)str 을 fmt 혁식에 박음
	return trans
#함수 안에 함수를 정의하는 이유 
#-> 웹의 특징: 다수가 접속하기 때문에 처음 들어온사람이 해당 함수를 만들면 후주자들은 해당 메모리에 함수를 사용하면 더 자원낭비가 적음


@app.route('/dt')
def dt():                      #value  #default value  # 
	datestr = request.values.get('date',date.today(), type=ymd('%Y-%m-%d')) #type 값으로는 함수(실제로는 메모리주소)가 들어가야한다
	return "우리나라 시간 형식: " + str(datestr)

#local.com:5000/sd 로 들어갈경우 호출
@app.route('/sd')
def helloworld_local():
    return  "Hello Local.com"

#g.local.com:5000/sd으로 들어가는 경우 
@app.route('/sd',subdomain="g")
def helloworlds():
    return "Hello G.Local.com"

@app.route('/rp')
def rp():
    q = request.args.get('q')
    return "q= %s" % str(q)


#localhost:5000/rp_list?ql=125&ql=000&ql=999
#rp_list = ['125','000','999'] 
@app.route('/rp_list')
def rp_list():
    lt = request.args.getlist('ql')
    return "q = %s" % str(lt)


@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        #header 는  전부 string 
        headers = [('Content-Type', 'text/plain'),
                    ('Content-Length',str(len(body)))]
        start_response('200 OK',headers)
        return [body]
    return make_response(application)

@app.route("/res1")
def res1():
    custom_res = Response("Custom Response",201, {'test':'ttt'})
    return make_response(custom_res)  #make_response  stream 으로 보냄


# @app.route("/gg")
# def helloworld_gg():
#     return "helloworld!!"+ getattr(g,'str','111')

@app.route("/")
def helloworld():
    return "Hello Flask World!"