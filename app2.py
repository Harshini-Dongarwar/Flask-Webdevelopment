
from flask import Flask, jsonify
from flask_restful import Api, Resource, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
   

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

subject_put_args = reqparse.RequestParser()
subject_put_args.add_argument("name", type=str, help="Name of the subject is required")

class SubjectResource(Resource):
    @marshal_with(resource_fields)
    def get(self, subject_id=None):
        if subject_id:
            result = Subject.query.filter_by(id=subject_id).first()
            if not result:
                return {'message': 'Subject not found'}, 404
            return result
        else:
            subjects = Subject.query.all()
            return subjects

    @marshal_with(resource_fields)
    def put(self, subject_id):
        args = subject_put_args.parse_args()
        subject = Subject.query.filter_by(id=subject_id).first()
        if subject:
            subject.name = args['name']
        else:
            subject = Subject(id=subject_id, name=args['name'])
            db.session.add(subject)
        db.session.commit()
        return subject
    def delete(self,subject_id):
        subject = Subject.query.filter_by(id=subject_id.first())

        db.session.delete(subject)
        db.session.commit()
        return{'message':"deleted"}
    


class BranchResource(Resource):
    @marshal_with(resource_fields)
    def get(self, branch_id=None):
        if branch_id:
            result = Branch.query.filter_by(id=branch_id).first()
            if not result:
                return {'message': 'branch not found'}, 404
            return result
        else:
            branch = Branch.query.all()
            return branch

    @marshal_with(resource_fields)
    def put(self, branch_id):
        args = subject_put_args.parse_args()
        branch1= Branch.query.filter_by(id=branch_id).first()
        if branch1:
            branch1.name = args['name']
        else:
            branch1 = Branch(id=branch_id, name=args['name'])
            db.session.add(branch1)
        db.session.commit()
        return branch1
    def delete(self,branch_id):
        branch = Branch.query.filter_by(id=branch_id).first()
        db.session.delete(branch)
        db.session.commit()
        return{'message':"deleted"}
    
    
    
    


api.add_resource(SubjectResource, "/subject", "/subject/<int:subject_id>")
api.add_resource(BranchResource, "/branch", "/branch/<int:branch_id>")

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
