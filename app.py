from flask import Flask, g, request, jsonify
from database import get_db
from functools import wraps

api_username = 'adm1n'
api_password = 'p4ssw9'

app = Flask(__name__)

def proteger(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'Usuario invalido'}),401
    return decorated
        

def jsonResult(members):
    return_values = []
    for member in members:
        member_dict = {}
        member_dict['id'] = str(member['id'])
        member_dict['name'] = member['name']
        member_dict['email'] = member['email']
        member_dict['level'] = member['level']
        return_values.append(member_dict)
    return return_values


@app.route('/member', methods = ['GET'])
@proteger
def get_members():
    db = get_db()
    members_cur = db.execute('''SELECT id, name, email, level FROM members''')
    members = members_cur.fetchall()
    return_values = jsonResult(members)
    return jsonify({'members':return_values})
    
    
@app.route('/member/<int:member_id>', methods = ['GET'])
@proteger
def get_member(member_id):
    db = get_db()
    qry = '''SELECT id, name, email, level FROM members WHERE id = {} '''.format(str(member_id))
    members_cur = db.execute(qry)
    members = members_cur.fetchone()
    return_values = jsonResult([members])
    return jsonify({'member':return_values[0]})

@app.route('/member', methods = ['POST'])
def add_member():
    new_member_data = request.get_json()
    name =  new_member_data['name']
    email =  new_member_data['email']
    level =  new_member_data['level']
    db = get_db()
    db.execute('INSERT INTO MEMBERS (NAME, EMAIL, LEVEL) VALUES (?,?,?)',[name, email, level])
    db.commit()

    
    return 'The name is {}, the email is {} and the level is {}'.format(name, email, level)

@app.route('/member/<int:member_id>', methods = ['PUT','PATCH'])
def edit_member(member_id):
    new_member_data = request.get_json()
    name =  new_member_data['name']
    email =  new_member_data['email']
    level =  new_member_data['level']

    db = get_db()
    db.execute('UPDATE members SET name = ?, email = ?, level = ? WHERE id = ?',[name, email, level, str(member_id)])
    db.commit()

    qry = '''SELECT id, name, email, level FROM members WHERE id = {} '''.format(str(member_id))
    members_cur = db.execute(qry)
    members = members_cur.fetchone()
    return_values = jsonResult([members])
    return jsonify({'member':return_values[0]})

@app.route('/member/<int:member_id>', methods = ['DELETE'])
def delete_member(member_id):
    db = get_db()
    qry = '''DELETE FROM members WHERE id = {} '''.format(str(member_id))
    db.execute(qry)
    db.commit()
    return jsonify({'member':'Usuario eliminado'})

if __name__ == "__main__":
    app.run(debug=True)
