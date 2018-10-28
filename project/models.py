from datetime import datetime

from flask_login import UserMixin, current_user
from sqlalchemy import and_, or_
from werkzeug.security import check_password_hash, generate_password_hash

from project import db


class User(UserMixin, db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String, unique=True, nullable=False)
	displayname = db.Column(db.String)
	#email               = db.Column(db.String, unique=True, nullable=False)
	is_admin = db.Column(db.Boolean,default=False, nullable=False )
	bio = db.Column(db.String, default="Hello, fellow ArtFlict users!")
	creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
	profile_pic_url = db.Column(db.String, nullable=True) 
	password_hash = db.Column(db.String, nullable=False)

	def __init__(self, username, displayname, password):
		self.username = username
		self.displayname = displayname
		self.set_password(password)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_followers(self):
		get_followers = Follower.query.filte_by(followedid=self.id)
		return get_followers

	def get_followed(self):
		get_followed = Follower.query.filte_by(followerid=self.id)
		return get_followed

	# def format_creation_date(self):
	# 	age = "ArtFlict age: "
	# 	now = datetime.now()
	# 	creation = self.creation_date
	# 	span = (now - creation).days
	# 	if days < 1:
	# 		age += "less than a day"
	# 	elif days == 1:
	# 		age += "1 day"
	# 	elif days < 365:
	# 		age += days + " days"
	# 	else:
	# 		years = (days/365)
	# 		if years == 1:
	# 			age += "1 year"
	# 		else:
	# 			age += years + " years"
	# 	return age


	def __repr__(self):
		return 'User %d %s' % (self.id, self.username)


class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	art_url = db.Column(db.String, nullable=True)
	artist_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
	title = db.Column(db.String, nullable=False)
	text = db.Column(db.String, nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
	art_link_creation_date = db.Column(db.DateTime, nullable=True)

	def __init__(self, author_id, title, text):
		self.author_id = author_id
		self.title = title
		self.text = text
		self.rating = 0

	def is_liked(self):
		userid = current_user.id
		getlike = Like.query.filter_by(userid=userid).filter_by(postid=self.id).first()
		if getlike:
			print(str(userid) + " likes " + str(self.id))
			return True
		return False

	def delete(self):
		 Like.query.filter_by(postid=self.id).delete()
		 db.session.delete(self)
		 db.session.commit()
		 return "deleted " + str(id)

	def relate(self):
		userid = current_user.id
		getpostlike = Like.query.filter_by(postid=self.id).filter_by(userid=userid).first()
		if getpostlike:
			db.session.delete(getpostlike)
			message = "like removed"
		else:
			add_like = Like(userid, self.id)
			db.session.add(add_like)
			message = "like added"
		db.session.commit()
		getlikes = Like.query.filter_by(postid=self.id).count()
		self.rating = getlikes
		db.session.commit()
		response = '{ "message": "' + message + '", "likes": "' + str(getlikes) + '"}'
		return response

	def link_art(self, art_url):
		self.art_url = art_url
		self.art_link_creation_date = datetime.now()

	def format_rating (self):
		rating = float(self.rating)
		if rating < 1000:
			return str(int(rating))
		elif rating < 1000000:
			new_rating = str(round(rating / 1000, 1))
			return new_rating + "K"
		elif rating < 1000000000:
			new_rating = round(rating / 1000000, 1)
			return new_rating + "M"
		else:
			return "OVER A BILLION HOLY SHIT"

	def format_date(self):
		now = self.creation_date
		print(self.title + " -->>> " + str(now))
		month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',
					  8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
		month = month_dict[now.month][:3]
		day_suffix = {1: 'st', 2: 'nd', 3:'rd'}
		last_digit = now.day % 10
		if now.day == 11 or now.day ==12 or now.day == 13:
			day_suffix = {1: 'th', 2: 'th', 3:'th'}
		if last_digit <= 3 and last_digit > 0:
			day = str(now.day) + day_suffix[last_digit]
		else:
			day = str(now.day) + 'th'
		return month + " " + day + " " + str(now.year)

	def __repr__(self):
		return "post " + str(self.id) + " " + str(self.title) + " " + str(self.text)


class Like(db.Model):
	__tablename__ = 'likes'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	postid = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

	def __init__(self, userid, postid):
		self.userid = userid
		self.postid = postid

	def __repr__(self):
		return "like " + str(self.id) + " " + str(self.userid) + " " + str(self.postid)


class Follower(db.Model):
	__tablename__ = 'followers'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	followerid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	followedid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	def __init__(self, followerid, followedid):
		self.followerid = followerid
		self.followedid = followedid

	def __repr__(self):
		return "like " + str(self.id) + " " + str(self.followerid) + " " + str(self.followedid)
