# 测试iptables 防火墙的拦截关键词是否成功。
## 如何使用
我们暂定封建关键词是 vname
### 启动测试服务器
```bash
docker run -it --rm -p 8000:8000  jockerdragon/webapi:tester
```
测试过程
```bash
# GET测试
[root@monther ~]# curl  192.168.157.129:8000
This is Flask Test Server
[/] -> show this menu
[/get] -> include keyword vvnnaammee
[/post] -> post to Test server
[root@monther ~]# curl 192.168.157.129:8000/get
cccccvname[root@monther ~]#

#POST测试
[root@monther ~]# curl -X POST 192.168.157.129:8000/post -H 'Content-Type: application/x-www-form-urlencoded'       -d 'vname=1232131'
[response.form.data] -> None
[response.form] -> ImmutableMultiDict([('vname', '1232131')])
[response] -> <Request 'http://192.168.157.129:8000/post' [POST]>
[requests.data] -> b''
```
### 在ROUTER上增加封禁规则
```bash
iptables -A FORWARD -p tcp -m string --string "vname" --algo bm --to 65535 -j DROP
````
### 效果是 GET /get 失效 POST中带有vname关键词失效

## 开发过程

Dockerfile
```dockerfile
FROM python:3.10.11
MAINTAINER <jockerdragon 2678885646@qq.com>
RUN pip install --upgrade pip
RUN pip install flask requests
EXPOSE 8000
WORKDIR /
ADD ./app.py /
CMD ["sh","-c","python app.py"]
```
 app.py
```python
root@ub-server:~# cat app.py
from flask import Flask, request

app = Flask(__name__)
#app.config['DEBUG'] = True
app.config['MAX_CONTENT_LENGTH'] = 1024000000

app.config.update(
    DEBUG=True,
    USE_X_SENDFILE=True,
#    MAX_CONTENT_LENGTH=2*1024*1024*1024
        )

@app.route('/post', methods=['POST'])
def post_post_handler():
    data = request.form.get('data')
    # 处理POST数据
    print(request.form)
    return f"[response.form.data] -> {data} \n[response.form] -> {request.form}\n[response] -> {request}\n[requests.data] -> {request.data}\n"


@app.route('/', methods=['GET'])
def root_get_handler():
    data = request.args.get('data')
    # 处理GET数据
    response = 'This is Flask Test Server\n[/] -> show this menu\n[/get] -> include keyword vvnnaammee\n[/post] -> post to Test server\n'
    return response

@app.route('/get', methods=['GET'])
def get_get_handler():
    data = request.args.get('data')
    # 处理GET数据
    response = 'cccccvname'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

```

