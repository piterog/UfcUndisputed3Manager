from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class EventForm(FlaskForm):
    description = StringField(
        'Event Name',
        validators=[
            DataRequired(message="Required field."),
            Length(min=3, max=70, message="The description must be between 3 and 70 characters long.")
        ],
        render_kw={"class": "form-control", "placeholder": "event name"}
    )
    
    submit = SubmitField('Save', render_kw={"class": "btn btn-primary"})