from app import db

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    members = db.relationship('GroupMember', backref='group', lazy='dynamic')
    expenses = db.relationship('Expense', backref='group', lazy='dynamic')
