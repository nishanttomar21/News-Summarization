from pymongo import MongoClient

client = MongoClient()
db = client.mydb
content = db.article_data

def insertion(title,image,url,summary,source,author):
    post = {"title": title,
            "url": url,
            "image": image,
            "summary": summary,
            "source": source,
            "author": author}
    content.insert_one(post)

def clear_values():
    content.remove({})
    
