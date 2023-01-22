from flask import Flask, request
import os

app = Flask(__name__)

if not os.path.exists("docker_bind"):
    os.makedir("docker_bind")

@app.route("/create_file",methods=["POST"])
def run():
    data = request.get_json()
    file_name, content =  data['file_name'], data['content']
    file_path = f"docker_bind/{file_name}"
    with open(file_path,'w') as write_file:
        write_file.write(content)
    return {"Status":"Success"}

app.run(debug=False,host='0.0.0.0',port = 5000)
