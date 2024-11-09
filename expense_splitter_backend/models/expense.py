from app import db

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    description = db.Column(db.String(256))
    amount = db.Column(db.Float, nullable=False)
    paid_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    category = db.Column(db.String(64))

    # Relationships
    splits = db.relationship('ExpenseSplit', backref='expense', lazy='dynamic')
