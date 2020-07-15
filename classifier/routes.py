import aiohttp
import asyncio
import uvicorn
import os
import secrets
import torch
import torchvision
from fastai.vision import *
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_uploads import UploadSet, configure_uploads, IMAGES
from classifier import app, db
from classifier.forms import ImageUploadForm
from classifier.models import User
from flask_login import login_user, current_user, logout_user, login_required

export_file_url = 'https://www.googleapis.com/drive/v3/files/1-B_IRObgJROvPR1wQ7RYrnwV4CXXE_Gu?alt=media&key=AIzaSyAjfbYsEA6D1_O4POidib22spKPwh_t_hk'
export_file_name = 'export.pkl'

classes = ['신봉선', '아이유', '한지민']
path=Path('classifier/data')
# path = Path(__file__).parent

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

# @app.route("/", methods = ['GET', 'POST'])
# def home():
#     form = ImageUploadForm()
#
#
@app.route("/", methods = ['GET', 'POST'])
@app.route("/home", methods = ['GET', 'POST'])
def home():
    form = ImageUploadForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            User.image_file = picture_file
            answer = classifier(picture_file)
            User.pred_class = answer
            db.session.commit()
            return redirect(url_for('upload'))
    return render_template('home.html', form=form)

@app.route("/upload", methods = ['GET', 'POST'])
def upload():
    form = ImageUploadForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    #         picture_file = save_picture(form.picture.data)
    #         User.image_file = picture_file
    #         answer = classifier(picture_file)
    #         User.pred_class = answer
    #         db.session.commit()
    image_file = url_for('static', filename='pics/'+ User.image_file)
    AIanswer= User.pred_class
    return render_template('upload.html', image_file=image_file, answer = AIanswer, form=form)


# @app.route("/upload", methods = ['GET', 'POST'])
# def upload():
#     form = ImageUploadForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#             picture_file = save_picture(form.picture.data)
#             User.image_file = picture_file
#             answer = classifier(picture_file)
#             User.pred_class = answer
#         db.session.commit()
#         return redirect(url_for('upload'))
#     image_file = url_for('static', filename='pics/'+ User.image_file)
#     AIanswer= User.pred_class
#     return render_template('upload.html', image_file=image_file, answer = AIanswer, form=form)

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def classifier(picture_file):
    await download_file(export_file_url, path / export_file_name)

    picture_path = os.path.join(app.root_path, 'static/pics', picture_file)
    # path=Path('classifier/data')
    learn = load_learner(path, export_file_name)
    img = open_image(picture_path)
    pred_class = learn.predict(img)[0]

    return pred_class


# def classify():
#     picture_path = os.path.join(app.root_path, 'static/pics', picture_file)
#     path=Path('classifier/data')
#     learn = load_learner(path)
#     img = open_image(picture_path)
#     pred_class,pred_idx,outputs = learn.predict(img)
#     return render_template('upload.html', image_file=image_file, answer = pred_class, form=form)






# 이거



# @app.route('/result', methods = ['GET', 'POST'])
# def result():
#     image_file = url_for('static', filename='pics/'+ current_user.image_file)
#     return render_template('result.html', title='결과', image_file = image_file)

# @app.route('/ask', methods = ['GET', 'POST'])
# def ask():
#     form = 버튼으로 yes / no알려주고, 정답 고르게 함
#     if form.validate_on_submit():
#         user = User(label=form.label.data)
#         db.session.add(user)
#         db.session.commit()
#         return redirect(url_for('감사합니다 page'))
#     return render_template('ask.html', form=form)
