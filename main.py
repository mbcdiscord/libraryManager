from flask import Flask,jsonify, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

#connect to mysql
def connection():
    return mysql.connector.connect(
        user='root',
        password='root',
        host='localhost',
        database='lbs'
    )

@app.route('/')
def index():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("select * from lib")
    books = cursor.fetchall()
    conn.close()
    cursor.close()
    return render_template('index.html', books=books)

@app.route('/run', methods=['POST'])
def run():
    cmd=request.form['cmd']
    conn=connection()
    cursor=conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/add',methods=['POST'])
def add():
    book = request.form['book']
    author=request.form['author']
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("INSERT INTO lib (BOOK, AUTHOR) VALUES (%s,%s)",(book,author))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lib WHERE BOOK LIKE %s", ('%' + query + '%',))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/students', methods=['POST'])
def students():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * from students")
    students=cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('students.html', students=students)

@app.route('/addStudent',methods=['POST'])
def addStudent():
    student = request.form['student']
    cls=request.form['class']
    conn=connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (NAME, CLASS) VALUES (%s,%s)',(student, cls))
    conn.commit()
    cursor.execute('select * from students')
    students=cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('students.html', students=students)

@app.route('/delStu/<int:id>',methods=['POST'])
def delStu(id):
    conn=connection()
    cursor=conn.cursor()
    cursor.execute('DELETE FROM students WHERE ROLL=%s',(id,))
    conn.commit()
    cursor.execute('select * from students')
    students=cursor.fetchall()
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/stuReset', methods=['POST'])
def stuReset():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute('ALTER TABLE students AUTO_INCREMENT=1')
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/ret',methods=['GET','POST'])
def ret():
    return redirect('/')


@app.route('/reset', methods=['POST'])
def reset():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute('ALTER TABLE lib AUTO_INCREMENT=1')
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/returned/<int:id>',methods=['POST'])
def returned(id):
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("UPDATE lib SET STATUS='available' WHERE ID=%s",(id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/dele/<int:id>', methods=['POST'])
def delete(id):
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("DELETE from lib where ID=%s",(id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')
@app.route('/borrowedB', methods=['POST'])
def borrowed():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.NAME, students.CLASS, students.BOOK, lib.ID
        FROM students
        JOIN lib ON students.BOOK = lib.BOOK
        WHERE lib.STATUS = 'borrowed'
    """)
    res = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('borrowed.html', res=res)


@app.route('/borrowB', methods=['GET','POST'])
def borrowB():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM lib WHERE STATUS = 'available' ")
    books=cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('borrow.html')

@app.route('/borrowBook', methods=['POST'])
def borrowBook():
    student = request.form['student']
    book=request.form['book']
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("UPDATE lib SET STATUS='borrowed' WHERE BOOK=%s",(book,))
    cursor.execute("UPDATE students SET BOOK=%s WHERE NAME=%s",(book,student))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/searchStudent')
def searchStudent():
    query = request.args.get('q', '')
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE NAME LIKE %s OR CLASS LIKE %s", 
                   ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

if __name__=='__main__':
    app.run(debug=True)