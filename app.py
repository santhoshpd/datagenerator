from flask import Flask, request, jsonify,json,send_file,render_template

from faker import Faker,Factory


app = Flask(__name__)
@app.route('/')
def index(): 
    return "<h1>DataGenerator</h1>"

@app.route("/input", methods=["GET","POST"])

def processjson():  
    if request.is_json:
        data = request.get_json()
        db=data['database']
        table=data['table_name']
        fields= data['fields']
        entries= data['entries']
        gender = ['Male', 'Female']
        fake = Faker()
        json_list=[]
        for i in range(entries):
            json_obj={}
            for k,v in fields.items():
                if v=="name":
                    json_obj[k]=fake.name()
                elif v=="email":
                    json_obj[k]=fake.email()
                elif v=="number":
                    json_obj[k]=fake.random_int(10, 100)
                elif v=="gender":
                    json_obj[k]=fake.random.choice(gender)
            json_list.append(json_obj)
        result = ''
        for element in  json_list:
            result += "insert into "+table+ " ("
            for i in element:
                if i==(list(element.keys())[-1]):
                    result += str(i)
                else:
                    result += str(i)+","
            result += ") values ("
            for i in element:
                if i==(list(element.keys())[-1]):
                    result += "'"+str(element[i])+"'"
                elif i=="age":
                    result += str(element[i])+","
                else:
                    result += "'"+str(element[i])+"',"
            result += ");\n"
        file_name = table+'.'+db
        files = open(file_name, 'w') 
        files.write(result) 
        files.close() 
        res=result.splitlines()
        response = {'insert_statements':res} 
        return response
    else:
        return jsonify({"message": "Request body must be JSON"}), 400

@app.route('/input/<filename>',methods=['GET','POST']) 
def downloadFile(filename):
   return send_file(filename, as_attachment=True) 


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')