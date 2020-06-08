from flask import Flask


app = Flask(__name__)

@app.route('/member', methods = ['GET'])
def get_members():
    return 'This return all the members'

@app.route('/member/<int:member_id>', methods = ['GET'])
def get_member(member_id):
    return 'This return by ID'

@app.route('/member', methods = ['POST'])
def add_member():
    return 'This return add new member.'

@app.route('/member/<int:member_id>', methods = ['PUT','PATCH'])
def edit_member(member_id):
    return 'This update a the members by ID'

@app.route('/member/<int:member_id>', methods = ['DELETE'])
def delete_member(member_id):
    return 'This remove a the members by ID'

if __name__ == "__main__":
    app.run(debug=True)
