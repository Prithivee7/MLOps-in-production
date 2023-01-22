from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/create_file",methods=["POST"])
def run():
    data = request.get_json()
    file_name, content =  data['file_name'], data['content']
    with open(file_name,'w') as write_file:
        write_file.write(content)
    return {"Status":"Success"}

app.run(debug=False,host='0.0.0.0',port = 5000)
