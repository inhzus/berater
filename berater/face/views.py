# -*- coding: utf-8 -*-
# created by inhzus

from flask import Blueprint, request

from berater.misc import Response, FaceStudentTable
from typing import List

face = Blueprint('face', __name__)


@face.route('students/id', methods=['GET'])
def get_student_ids():
    params = {
        'department': request.args.get('department', None),
        'origin': request.args.get('origin', None),
        'stuid': request.args.get('stuid', None)
    }
    params = {k: v for (k, v) in params.items() if v is not None}
    students: List[FaceStudentTable] = FaceStudentTable.query.filter_by(**params).all()
    student_ids = [student.stuid for student in students]
    return Response(stu_list=student_ids).json()
