import sqlite3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livros.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


def run_sql_script(script_filename):
    connection = sqlite3.connect('livros.db')
    with open(script_filename, 'r') as script_file:
        script = script_file.read()
        try:
            connection.executescript(script)
            print("SQL script executed successfully")
        except sqlite3.Error as e:
            print(f"Error executing SQL script: {e}")
        finally:
            connection.close()


with app.app_context():
    db.create_all()
    run_sql_script('init_db.sql')


@app.route('/livros', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        books_list = Book.query.all()
        books = [{'id': book.id, 'title': book.title, 'author_id': book.author_id} for book in books_list]
        return jsonify({'livros': books})
    elif request.method == 'POST':
        title = request.json['title']
        author_id = request.json['author_id']
        new_book = Book(title=title, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'mensagem': 'Livro adicionado com sucesso'})


@app.route('/autores', methods=['GET', 'POST'])
def authors():
    if request.method == 'GET':
        authors_list = Author.query.all()
        authors = [{'id': author.id, 'name': author.name} for author in authors_list]
        return jsonify({'autores': authors})
    elif request.method == 'POST':
        name = request.json['name']
        new_author = Author(name=name)
        db.session.add(new_author)
        db.session.commit()
        return jsonify({'mensagem': 'Autor adicionado com sucesso'})


if __name__ == '__main__':
    app.run(debug=True)
