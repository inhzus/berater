# -*- coding: utf-8 -*-
# created by inhzus

from flask_sqlalchemy import SQLAlchemy

engine = SQLAlchemy()


class CandidateTable(engine.Model):
    __tablename__ = 'candidate'
    openid = engine.Column(engine.String(30), primary_key=True)
    phone = engine.Column(engine.String(20), nullable=False)
    name = engine.Column(engine.String(16), nullable=False)
    province = engine.Column(engine.String(2), nullable=False)
    city = engine.Column(engine.String(10), nullable=False)
    score = engine.Column(engine.Float(precision=1), nullable=False)


class StudentTable(engine.Model):
    """The fresh"""
    __tablename__ = 'student'
    openid = engine.Column(engine.String(30), primary_key=True)
    phone = engine.Column(engine.String(20), nullable=False)
    id_card = engine.Column(engine.String(18), nullable=False)
    admission_id = engine.Column(engine.String(16))
    student_id = engine.Column(engine.String(12))


class FaceStudentTable(engine.Model):
    __tablename__ = 'face_student'
    # __bind_key__ = 'local'
    stuid = engine.Column(engine.String(12), primary_key=True)
    origin = engine.Column(engine.String(10), index=True)
    gender = engine.Column(engine.String(2))
    department = engine.Column(engine.String(32), index=True)

    def to_dict(self):
        return dict(stuid=self.stuid, origin=self.origin, gender=self.gender, department=self.department)
