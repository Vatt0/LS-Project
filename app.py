# /news - endpointi yvela newsis chveneba
# /news/id - mititebuli idis mkone news-i

from datetime import datetime
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dbase.db"
db = SQLAlchemy(app)

class NewsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"News(title={title},description={description},category={category},date={date},author={author})"


news_put_args = reqparse.RequestParser()
news_put_args.add_argument("title", type=str, help="title of the news is required",required=True)
news_put_args.add_argument("description", type=str, help="description of the news is required",required=True)
news_put_args.add_argument("category", type=str, help="category of the news is required",required=True)
news_put_args.add_argument("date", type=datetime)
news_put_args.add_argument("author", type=str, help="author of the news is required",required=True)

news_update_args = reqparse.RequestParser()
news_update_args.add_argument("title", type=str, help="title of the news is required")
news_update_args.add_argument("description", type=str, help="description of the news is required")
news_update_args.add_argument("category", type=str, help="category of the news is required")
news_update_args.add_argument("author", type=str, help="author of the news is required")


resource_field ={
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'category': fields.String,
    'date': fields.DateTime,
    'author': fields.String
}

class News(Resource):

    #ert-erti news-is wamogheba id-it
    @marshal_with(resource_field)
    def get(self, news_id):
        result = NewsModel.query.filter_by(id=news_id).first()
        if not result:
            abort(404, message="Am ID-it news ver moidzebna")
        
        return result

    #news-is damateba
    @marshal_with(resource_field)
    def post(self, news_id):
        args = news_put_args.parse_args()
        result = NewsModel.query.filter_by(id=news_id).first()
        if result:
            abort(409,message="Mititebuli ID dakavebulia")

        news = NewsModel(id=news_id, title=args['title'], description=args['description'], category=args['category'], date=args['date'], author=args['author'] )
        db.session.add(news)
        db.session.commit()
        return news, 201

    #news-is ganaxleba
    def put(self, news_id):
        args = news_update_args.parse_args()
        result = NewsModel.query.filter_by(id=news_id).first()
        if not result:
            abort(404, message="Mititebuli ID-it news ver moidzebna, ver ganaxldeba")
        if args['title']:
            result.title = args['title']
        if args['description']:
            result.description = args['description']
        if args['category']:
            result.category = args['category']
        if args['author']:
            result.author = args['author']

        db.session.commit()

    #news-is washla
    def delete(self, news_id):
        result = NewsModel.query.filter_by(id=news_id).first()
        if result:
            db.session.delete(result)
            db.session.commit()
        return '',204

class AllNews(Resource):
    #yvela news-is chveneba
    @marshal_with(resource_field)
    def get(self):
        data = NewsModel.query.all()
        result = [d.__dict__ for d in data]
        return result
 

api.add_resource(News, "/news/<int:news_id>")
api.add_resource(AllNews, "/news")


if __name__ == "__main__":
    app.run(debug=True)