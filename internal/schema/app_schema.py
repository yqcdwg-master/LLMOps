from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CompletionReq(FlaskForm):
    query = StringField("query", validators=[
        DataRequired("用户提问必填"),
        Length(min=1, max=2000, message="用户的最大提问长度问 2000")
    ])
