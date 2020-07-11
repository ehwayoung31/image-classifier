from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

class ImageUploadForm(FlaskForm):
    picture = FileField('사진을 업로드해주세요.', validators=[FileAllowed(['jpg','png', 'jfif'])])
    retry = SubmitField('다시 해보기')
    submit =  SubmitField('업로드', render_kw = {"onsubmit":"myFunction()"})

    # def validate_picture(self, picture):
    #     if not picture:
    #         raise ValidationError('이미지 형식이 잘못되었습니다.')

# class AnswerForm(FlaskForm):
#     Yes = BtnField('')
#     No = BtnField('')
