from flask import Flask, request, render_template, json, jsonify
from flask_cors import CORS
from demo import Demo
import os

import exports_bpy

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024
CORS(app)

@app.route('/clothes', methods=['GET', 'POST'])
def index():
    # request.form에서 데이터 추출
    root = request.form.get('root', './uploads/stylechain/product/img')
    out = request.form.get('out', './uploads/stylechain/product/3d')
    mesh = request.form.get('mesh', './meshes')
    checkpoints = request.form.get('checkpoints', './checkpoints')
    garment_type = request.form.get('garment_type', 'pants')
    front = request.form.get('front', None)
    back = request.form.get('back', None)

    out = './uploads/stylechain/product/3d/' + out

    os.makedirs(out, exist_ok=True)

    # Demo 클래스에 매개변수 전달
    demo = Demo(root, out, mesh, checkpoints, garment_type, front, back)
    demo.run()
    demo.clear_tmp()

    exports_bpy.exports_3dModeling(out)

    return jsonify({
        'result': 'true'
    })

if __name__ == "__main__":
    app.run("0.0.0.0")