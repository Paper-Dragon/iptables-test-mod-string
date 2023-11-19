from flask import Flask, request

app = Flask(__name__)
# app.config['DEBUG'] = True
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
