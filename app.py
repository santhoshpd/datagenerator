from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/')
def index(): 
    return '<h1>DataGenerator</h1>'

@app.route("/", methods=["POST"])
def processjson():  
    if request.is_json:
        data = request.get_json()
        table=data['table_name']
        fields= data['list_field']
        entries= data['entries']
    #return jsonify({'table':table,'fields':fields,'entries':entries})
        #response_body = {
        #    "message": "JSON received!",
        #    'table':table,
        #    'fields':fields,
        #    'entries':entries
        #}
        #res = jsonify(response_body), 200
        #return res
        from mimesis.schema import Field, Schema
        from mimesis.enums import Gender
        _ = Field('en')
        dummy_users = Schema(
            lambda: {
                'name': _('name'),
                'gender': _('gender'),
                'email': _('email'),
                'age': _('age'),
            }
        )
        dummy_data = dummy_users.create(iterations=entries)
        return jsonify(dummy_data),200
    else:
        return jsonify({"message": "Request body must be JSON"}), 400


if __name__ == '__main__':
    app.run(debug=True)