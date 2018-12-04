import os
from urllib.parse import urlparse

from flask import (Blueprint, Response, abort, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required

from project import db
from project.forms import *
from project.models import Like, Post, User

from . import app


@app.route('/') #default
def landingpage():
	if not current_user:
		return redirect("/login")
	return redirect("/feed")

@app.route('/feed', methods=['GET'])
@login_required
def feed():
	sort_by = request.args.get("sort_by")
	show = request.args.get("show")
	order = request.args.get("order")

	if not sort_by:
		sort_by = "new"
	if not show:
		show = "all"
	if not order:
		order = "normal"

	sort_list = {"new": "New","top":"Top","alphabetical":"A-Z"}
	show_list = {"all":"All","artless":"Artless","with-art":"With Art"}
	order_list = {"normal":"Normal", "reverse":"Reverse"}

	if sort_by not in sort_list.keys() or show not in show_list.keys() or order not in order_list.keys():
		abort(404)

	if sort_by == "top":
		if order == "normal":
			posts = Post.query.order_by(Post.rating.desc()).order_by(Post.title.asc())
		else:
			posts = Post.query.order_by(Post.rating.asc()).order_by(Post.title.asc())

	elif sort_by == "alphabetical" :
		if order == "normal":
			posts = Post.query.order_by(Post.title.asc())
		else:
			posts = Post.query.order_by(Post.title.desc())

	elif sort_by == "new":
		if order == "normal":
			posts = Post.query.order_by(Post.creation_date.desc())
		else:
			posts = Post.query.order_by(Post.creation_date.asc())

	else:
		return "what"

	if show == "with-art":
		posts = posts.filter(Post.art_url != None)
	elif show == "artless":
		posts = posts.filter(Post.art_url == None)

	posts = posts.all()

	filters = { "sort_by":sort_list[sort_by] , "show":show_list[show] , "order": order_list[order]}

	return render_template('feed.html', posts=posts, filters = filters)

@app.route('/profile')
@login_required
def my_profile():
	username = current_user.username
	print(username)
	return redirect("/profiles/" + username)


@app.route('/profiles/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
	visited_user = User.query.filter_by(username=username).first()
	pic_form = ProfilePicForm(request.form)
	bio_form = ProfileBioForm(request.form)
	if request.method == 'GET':
		print("visited user")
		return render_template('profile.html', visited_user=visited_user)
	else:
		abort(404)


@app.route('/relate/<int:id>', methods=['POST'])
@login_required
def relate(id):
	post = Post.query.filter_by(id=id).first()
	return post.relate()

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
	post = Post.query.filter_by(id=id).first()
	id = post.id
	if post.author_id == current_user.id or current_user.is_admin:
		Like.query.filter_by(postid=post.id).delete()
		db.session.delete(post)
		db.session.commit()
		print("deleted --> " + str(id))
		return redirect(url_for('feed'))
	else:
		return "action not allowed"

@app.route('/add', methods=['GET','POST'])
def add_post():
	form = PostForm(request.form)
	if request.method == 'GET':
		return render_template('add_post.html', form = form)
	else:
		title = form.title.data
		text = form.text.data
		post = Post(current_user.id, title, text)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('feed'))


@app.route('/about')
def aboutus():
	return render_template('about_page.html')



@app.route('/stories/<int:post_id>', methods=['GET', 'POST'])
@login_required
def show_story(post_id):
	form = AddArtForm(request.form)
	if request.method == "GET":
		post = Post.query.filter_by(id=post_id).first()
		return render_template('story-view.html', post=post)
	else:
		print("posting in sroty view")
		pass


@app.route('/illustrate/<int:post_id>', methods=['POST'])
@login_required
def illustrate(post_id):
	folder_name = "static/uploaded_art/post_{}/"

	target = os.path.join(app.config["PROJECT_DIR"], folder_name.format(post_id) )
	print(target)

	if not os.path.isdir(target):
		os.mkdir(target)

	print(request.files["file"])

	upload = request.files["file"]
	print("{} is the file name".format(upload.filename))
	filename = upload.filename
	# This is to verify files are supported
	ext = os.path.splitext(filename)[1]
	if (ext == ".jpg") or (ext == ".png"):
		print("File supported moving on...")
	else:
		return "not accepted :C"
	destination = "/".join([target, filename])
	print("Accept incoming file:", filename)
	print("Save it to:", destination)
	upload.save(destination)

	# return send_from_directory("images", filename, as_attachment=True)
	return redirect(url_for('show_story', post_id=post_id))
