from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np
import mysql.connector


popular_df = pd.read_pickle(open('popular.pkl', 'rb'))
pt = pd.read_pickle(open('pt.pkl', 'rb'))
books = pd.read_pickle(open('books.pkl', 'rb'))
similarity_scores = pd.read_pickle(open('similarity_scores.pkl', 'rb'))
books_data = pd.read_pickle(open('books_data.pkl', 'rb'))
authors = pd.read_pickle(open('authors.pkl', 'rb'))


app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rivi",
    database="Lumosdb"
)
cursor = db.cursor()

cursor.execute("USE Lumosdb")
db.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_ratings'].values),
                           rating = list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:9]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)

    return render_template('recommend.html', data=data)

@app.route("/contact", methods=['GET', 'POST'])
def contact_ui():
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['Email']
        message = request.form['Message']
        
        # Insert form data into ContactForm table
        cursor.execute("INSERT INTO ContactForm (Name, Email, Message) VALUES (%s, %s, %s)", (name, email, message))
        db.commit()
        
        return "Thank you for your message!"
    else:
        return render_template('contact.html')
    #return render_template("contact.html")

@app.route("/listofauthors")
def listofA():
    return render_template("listofauthors.html", authors=authors)

# @app.route("/booksbyauthors", methods=['GET'])
# def booksbyA():
    # author_name = request.form.get('author_name')

    # # Filter the DataFrame to get books by the specified author
    # author_books = booksbyA_df[booksbyA_df['Book-Author'] == author_name]

    # # Prepare the data to be passed to the template
    # data = []
    # for index, row in author_books.iterrows():
    #     item = {
    #         'title': row['Book-Title'],
    #         'author': row['Book-Author'],
    #         'image_url': row['Image-URL-M']
    #     }
    #     data.append(item)

    # return render_template('booksbyauthors.html', author_name=author_name, books=data)
    # author_name = request.form.get('author_name')
    # author_books = books_data[books_data["Book-Author"] == author_name]
    # if author_books.empty:
    #     return render_template('booksbyauthors.html', author_name=author_name, books=None)
    # else:
    #     book_info = []
    #     for index, row in author_books.iterrows():
    #         book_info.append({
    #             'title': row['Book-Title'],
    #             'author': row['Book-Author'],
    #             'year': row['Year-Of-Publication'],
    #             'image_url': row['Image-URL-M']
    #         })
    #     return render_template('booksbyauthors.html', author_name=author_name, books=book_info)
    # author_name = request.form.get('Book-Author')
    # author_books = books_data[books_data["Book-Author"] == author_name]
    # if author_books.empty:
    #     return render_template('booksbyauthors.html', author_name=author_name, books=None)
    # else:
    #     book_info = []
    #     for index, row in author_books.iterrows():
    #         book_info.append({
    #             'title': row['Book-Title'],
    #             'author': row['Book-Author'],
    #             'year': row['Year-Of-Publication'],
    #             'image_url': row['Image-URL-M']
    #         })
    #     return render_template('booksbyauthors.html', author_name=author_name, books=book_info)

@app.route("/booksbyauthors", methods=['GET'])
def booksbyA():
    if request.method == 'GET':
        return render_template('booksbyauthors.html', author_name=None, books=None)
        
    print("Request args:", request.args)
    author_name = request.args.get('Book-Author')
    author_books = books_data[books_data["Book-Author"] == author_name]
    if author_books.empty:
        return render_template('booksbyauthors.html', author_name=author_name, books=None)
    else:
        book_info = []
        for index, row in author_books.iterrows():
            book_info.append({
                'title': row['Book-Title'],
                'author': row['Book-Author'],
                'year': row['Year-Of-Publication'],
                'image_url': row['Image-URL-M']
            })
        return render_template('booksbyauthors.html', author_name=author_name, books=book_info)



@app.route("/publish", methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':
        name = request.form['Name']
        review = request.form['Review']
        
        # Insert form data into ContactForm table
        #cursor.execute("INSERT INTO Reviews (Name, Review) VALUES (%s, %s)", (name, review))
        cursor.execute("INSERT INTO Reviews (name, review) VALUES (%s, %s)", (name, review))

        db.commit()
        
        return "Thank you for your review!"
    else:
        return render_template('publish.html')
    #return render_template("publish.html")

@app.route("/review")
def review():
    cursor.execute("SELECT name, review FROM Reviews")
    reviews_data = cursor.fetchall()
    print("Fetched reviews:", reviews_data)
    return render_template('review.html', reviews=reviews_data)
    #return render_template("review.html")

if __name__ == '__main__':
    app.run(debug = True)