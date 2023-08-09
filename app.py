from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from bson.objectid import ObjectId

# 파이몽고 연결하기
from pymongo import MongoClient
client = MongoClient('mongodb+srv://pmaker126:test@cluster0.pemxrix.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')


# 몽고DB에 닉네임, 이메일, 비밀번호 데이터 넣기
@app.route("/login", methods=["POST"])
def login():
    nickname_receive = request.form['nick_give']
    email_receive = request.form['email_give']
    password_receive = request.form['pw_give']

    doc = {
        'nick': nickname_receive,
        'email': email_receive,
        'pw': password_receive
    }
    db.todo.insert_one(doc)
    return jsonify({'msg': '입력 완료!'})


# 몽고DB에 to-do-list 데이터 넣기
@app.route("/todo", methods=["POST"])
def todo_post():
    date_receive = request.form['date_give']
    list_receive = request.form['list_give']

    doc = {
        'date': date_receive,
        'list': list_receive,
        'done' : 0
    }
    db.todo.insert_one(doc)
    return jsonify({'msg': '입력 완료!'})


#투두 리스트 완료 체크할 때
@app.route("/todo/done", methods=["POST"])
def todo_done():
    id_receive = request.form['id_give']
    db.todo.update_one({'_id': ObjectId(id_receive)}, {'$set': {'done': 1}})

    return jsonify({'msg': '완료!'})

#투두 완료 취소 
@app.route("/todo/cancel", methods=["POST"])
def todo_cancel():
    id_receive = request.form['id_give']
    db.todo.update_one({'_id': ObjectId(id_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '완료 취소!'})

#투두 삭제
@app.route("/todo/delete", methods=["POST"])
def todo_delete():
    id_receive = request.form['id_give']
    db.todo.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({'msg': '삭제 완료'})

#몽고디비에서 num 값 대신 ID값 가져오기
@app.route("/todo", methods=["GET"])
def todo_get():
    todo_memo_list = list(db.todo.find())

    for i in range(len(todo_memo_list)):
        todo_memo_list[i]['_id'] = str(todo_memo_list[i]['_id'])
    return jsonify({'todo_memos': todo_memo_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
