from src import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    
    firebase_uid = db.Column(db.String(200), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=True)
    name = db.Column(db.String(200), nullable=True)
    photo_url = db.Column(db.String(500), nullable=True)
    role = db.Column(db.String(50), nullable=False, default="user")
    provider = db.Column(db.String(50), nullable=False, default="password")
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now()
    )
    last_login = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User {self.email}>"
