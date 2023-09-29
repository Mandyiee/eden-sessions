from app import db
import uuid
import datetime

class Image(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False,index=True)
    name = db.Column(db.String(64),nullable=True)
    image_file = db.Column(db.String(20),nullable=True)
    text = db.Column(db.Text,nullable=True)
    html_text = db.Column(db.Text,nullable=True)
    lexer = db.Column(db.String(64),nullable=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<Trying %r>' % self.name
