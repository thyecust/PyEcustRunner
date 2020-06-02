from flask import Flask, session, request, render_template, make_response
import json
from Campus import Campus
from math import ceil
import base64
import matplotlib.pyplot as plt
from io import BytesIO
import cv2
from PyerImg import get_border, get_vias_lnglat
from PyerPointRecognize import get_point

app = Flask(__name__)
app.secret_key = 'python 2020 spring'
app.debug = True

@app.route("/", methods=['GET', 'POST'])
def index():
    with open('./graph.json') as f:
        content = f.read()
        session['graph'] = json.loads(content)
        session['priority'] = [20,59,63,66,67,72]
    return render_template("inface.html")

@app.route("/cross", methods=['GET', 'POST'])
def get_cross():
    with open('./cross.json','r') as f:
        content = f.read()
        return content

@app.route("/graph", methods=['GET', 'POST'])
def get_graph():
    with open('./graph.json','r') as f:
        content = f.read()
        return content

@app.route('/path',methods = ['POST', 'GET'])
def path():
    graph = session['graph']
    priority = session['priority']
    campus = Campus(graph,priority)

    ae=json.loads(request.args.get('ae'))
    for item in ae:
        campus.add_edge(item)

    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    path = campus.get_path(start,end)
    return json.dumps(path)

@app.route('/path2',methods = ['POST', 'GET'])
def path2():
    graph = session['graph']
    priority = session['priority']
    campus = Campus(graph,priority)

    ae=json.loads(request.args.get('ae'))
    for item in ae:
        campus.add_edge(item)
        
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    vias = json.loads(request.args.get('vias'))
    path = campus.get_path(start,end,vias)
    return json.dumps(path)

@app.route('/path3',methods=['GET','POST'])
def path3():
    graph = session['graph']
    priority = session['priority']
    campus = Campus(graph,priority)

    ae=json.loads(request.args.get('ae'))
    for item in ae:
        campus.add_edge(item)
    
    length = int(request.args.get('length'))
    start = int(request.args.get('start'))
    priority = int(request.args.get('priority'))
    vias = json.loads(request.args.get('vias'))
    path = campus.get_fixed_path(start,vias,length,priority)
    return path

@app.route('/img/<filepath>',methods=['GET'])
def img(filepath):
    image_data = open('./img/'+filepath, "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/test',methods=['GET'])
def test():
    s1 = request.args.get('s2')
    if s1:
        r1 = json.loads(s1)
        return json.dumps(r1)
    else:
        return 'no in'

@app.route('/upload',methods=['POST'])
def upload():
    data = request.get_data()
    sdata = str(data)[2:-1]
    b64bin = sdata.split(',')[1]
    img_type = sdata.split(';')[0][11:]
    img_bin = base64.b64decode(b64bin)
    img = plt.imread(BytesIO(img_bin),img_type)
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    
    (x,y),(w,h),angle = get_border(img)
    cl = get_point(img)
    result = get_vias_lnglat(x,y,w,h,angle,cl,img.shape)
    return json.dumps(result)

if __name__ == "__main__":
    app.run()
    # app.run(host='0.0.0.0',port=5000)