from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
from re import sub
popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
# pt = pickle.load(('pt.pkl')
books = pickle.load(open('books.pkl','rb'))
avg_ratings = pd.read_pickle('avg_ratings.pkl')
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
popular_df = pd.DataFrame(popular_df)
pt = pd.DataFrame(pt)
books = pd.DataFrame(books)
app = Flask(__name__)

@app.route('/')
def ui():
    return render_template('home.html')

@app.route('/home')
def home_ui():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html',
                        book_name = list(popular_df['Book-Title'].values),
                        author=list(popular_df['Book-Author'].values),
                        image=list(popular_df['Image-URL-M'].values),
                        votes=list(popular_df['Num-Ratings'].values),
                        rating=(list(np.round(popular_df['Avg-Rating'].values,1)))
                        
                        )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books_byauth',methods=['post'])
def recommend_author():
    user_input_auth = request.form.get('user_input_auth').capitalize()   
    ans=[]
    temp_df = books.loc[books['Book-Author'].str.contains(user_input_auth,case=False)]
    temp_df = temp_df[['Book-Title', 'Book-Author' , 'Image-URL-M']]
    temp_df=temp_df.merge(avg_ratings,on='Book-Title').drop_duplicates('Book-Title')
    temp_df['Avg-Rating']=round(temp_df['Avg-Rating'],1)
    ans=temp_df.values.tolist()
    list2 = []
    for i in ans:
        if i not in list2:
            list2.append(i)
        
    list2[0:10]
    return render_template('recommend.html',data2=list2)

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input').capitalize()
    res = [i for i in pt.index if user_input in i]
    print(res)
    
    data=[]
    similar_books = []
    indexes = set()
    for i in res:
        index = np.where(pt.index==i)[0][0]
        indexes.add(index)
        similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:8]
        for k in similar_items:
            if k not in similar_books:
                similar_books.append(k)

    matched_list= list(indexes)
    indexes=set()
    for k in similar_books:
        indexes.add(k[0])
        
    similar_list=list(indexes) 
    output_indices = []
    for item in matched_list:
        if item not in output_indices:
            output_indices.append(item)
    for item in similar_list:
        if item not in output_indices:
            output_indices.append(item)    
    ans=[]
    df1 =books['Book-Title'].apply
    for j in output_indices:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[j]]
        temp_df2 = avg_ratings[avg_ratings['Book-Title'] == pt.index[j]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(np.round(temp_df2.drop_duplicates('Book-Title')['Avg-Rating'].values,1)))
        item.extend(list(temp_df2.drop_duplicates('Book-Title')['Num-Ratings'].values))
        ans.append(item)
    ans[0:10]
    return render_template('recommend.html',data=ans)

if __name__ == '__main__':
    app.run(debug=True)