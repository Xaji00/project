from flask import jsonify,request
from flask_restful import Resource
from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,current_user,logout_user,login_required
from functools import wraps


from flask_proj.db import session
from flask_proj.app import app,api,login_manager
from flask_proj.models import Review,User,Comments




@login_manager.user_loader
def load_user(user_id):
     return session.get(User,user_id)




def admin_required(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.admin != True: 
            return jsonify({'massage' : 'Вы не админ'})
        return func(*args, **kwargs)
    return decorated_view





def author_or_admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        review_id = kwargs.get('review_id')
        review  = session.query(Review).filter_by(id=review_id).first()
        if not review:
            return jsonify({'message': 'Отзыв не найден'})
        

        if current_user.username != review.author and current_user.admin != True: 
            return jsonify({'message': 'У вас нет доступа'})
        
        return func(*args, **kwargs)
    return decorated_view






class UserLogout(Resource):
    def get(self):
        logout_user()
        return jsonify({'Logout' : 'success'})




class UserLogin(Resource):
     def post(self):
          username = request.json.get("username")
          password = request.json.get("password")
          user = session.query(User).filter_by(username=username).first()
          if user and check_password_hash(user.password_hash,password):
            login_user(user)
            return jsonify({'massage' : f'Добро пожаловать {current_user.username}'})
          else:
              return jsonify({"massage" : "пользователь не найден или неверный логин или пароль"})



class Main(Resource):

    def get(self):
            reviews_data = session.query(Review).all()
            reviews_json = [{'title': reviews.title, 'text': reviews.text} for reviews in reviews_data]  
            return jsonify(reviews_json)
    
    @login_required
    def post(self):
         reviews_data = request.json
         review = Review(text=reviews_data['text'],title=reviews_data['title'],author=current_user.username)
         session.add(review)
         session.commit()
         return jsonify({'Добавлено': 201})
    

class DetailPost(Resource):
    @login_required
    def get(self,review_id):
        review = session.query(Review).filter_by(id=review_id).first()
        if review:
            data = [{'id': review.id , 'title' : review.title, 'text' : review.text, 'author' : review.author,'comments' : [{'author' : comment.author,'text' : comment.text} for comment in review.comments]}]
            return jsonify(data)
        else:
            return jsonify({'massage' : "Отзыв не найден"})
     

    @login_required
    @author_or_admin_required
    def delete(self,review_id):
        review = session.query(Review).filter_by(id=review_id).first()
        if review:
            session.query(Comments).filter_by(review_id=review_id).delete()
            session.delete(review)
            session.commit()
            return jsonify({'message' : f'Отзыв удалён'})
        else:
            return jsonify({'message': "Отзыв не найден"})
          
     
    @login_required
    @author_or_admin_required
    def put(self,review_id):
        title = request.json.get("title")
        text = request.json.get("text")
        review = session.query(Review).filter_by(id=review_id).first()
        if review:
            review.title = title
            review.text = text
            session.commit()
            return jsonify({'massage' : "Отзыв обновлён"})
        else:
            return jsonify({'message': "Отзыв не найден"})


class AddComment(Resource):
    @login_required
    def post(self,review_id):
         commentdata = request.json
         comments = Comments(text=commentdata['text'],author=current_user.username,review_id=review_id)
         review = session.query(Review).filter_by(id=review_id).first()
         if review:
            session.add(comments)
            session.commit()
            return jsonify({'massage' : "Коментарий добавлен"})
         else:
             return jsonify({'massage' : "Отзыв не найден"})

class AddUser(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        lastname = request.json.get("lastname")

        if username is None or password is None or lastname is None:
            return abort(400)
        password_hash = generate_password_hash(password)
        user = User(username=username,password_hash=password_hash,lastname=lastname)
        session.add(user)
        session.commit()
        return jsonify({'Welcome' : user.username}, 201)
        


class UserList(Resource):
    @login_required
    def get(self):
        users = session.query(User).all()
        return jsonify({"users" : [{'username' : user.username, "id" : user.id,"lastname" : user.lastname} for user in users]})
    
class UserDelete(Resource):
    @admin_required
    def delete(self,user_id):
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return jsonify({"massage":'Пользователь удалён'})
        else:
            return jsonify({"massage":'пользователь не найден'})




api.add_resource(UserList,'/users')
api.add_resource(UserLogout,'/logout')
api.add_resource(UserLogin,'/login')
api.add_resource(AddUser,'/adduser')
api.add_resource(Main,"/main")
api.add_resource(DetailPost,"/main/<int:review_id>")
api.add_resource(AddComment,'/comment/<int:review_id>')
api.add_resource(UserDelete,'/delete_user/<int:review_id>')
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True,port=8080)