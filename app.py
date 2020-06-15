from flask import Flask, request, jsonify,json,send_file,render_template
import random
from faker import Faker,Factory

app = Flask(__name__)
@app.route('/')
def index(): 
    return "<h1>DataGenerator</h1>"

@app.route("/input", methods=["GET","POST"])
def process_json():  
    data = request.get_json()
    db=data['database']
    table=data['table_name']
    fields= data['fields']
    entries= data['entries']
    gender = ['Male', 'Female']
    fake = Faker()
    json_list=[]
    result = ''
    for i in range(entries):
        json_obj={}
        result += "insert into "+table+ " ("
        for i in fields:
            if i==(list(fields.keys())[-1]):
                result += str(i)
            else:
                result += str(i)+","
        result += ") values("
        for key,value in fields.items():
            for k,v in value.items():
                if v=="name":
                    json_obj[key]=fake.name()
                if v=="first_name":
                    json_obj[key]=fake.first_name()
                if v=="last_name":
                    json_obj[key]=fake.last_name()
                if v=="address":
                     json_obj[key]=fake.address()
                elif v=="email":
                    json_obj[key]=fake.email()
                elif v=="gender":
                    json_obj[key]=fake.random.choice(gender)
                elif v=="number":
                    if ("minimum" in value) or ("maximum" in value):
                        json_obj[key]=random.randint(value['minimum'],value['maximum'])
                    else:
                         json_obj[key]=fake.random_number()
                    if key==(list(fields.keys())[-1]):
                        result += str(json_obj[key])
                    else:
                        result += str(json_obj[key])+","
                    break
                if key==(list(fields.keys())[-1]) and v!="number":
                    result += "'"+str(json_obj[key])+"'"
                elif key!=(list(fields.keys())[-1]) and v!="number":
                    result += "'"+str(json_obj[key])+"',"
        json_list.append(json_obj)
        result += ");\n"
    #print(json_list)    
    #print(result)
    file_name = table+'.'+db
    files = open(file_name, 'w') 
    files.write(result) 
    files.close() 
    #res=result.splitlines()
    #response = {'insert_statements':res} 
    #return response
    return send_file(file_name, as_attachment=True) 

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')