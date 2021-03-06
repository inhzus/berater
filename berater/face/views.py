# -*- coding: utf-8 -*-
# created by inhzus

from typing import List

from flask import Blueprint, request
from flask_sqlalchemy import orm
from sqlalchemy import or_

from berater.misc import Response, SourceStudentTable, engine
from berater.utils import token_required, Permission

face = Blueprint('face', __name__)


@face.route('/students', methods=['GET'])
@token_required(role=Permission.FACE)
def get_students():
    params = {k: request.args.get(k, '') for k in ['department', 'admission_id', 'origin', 'field', 'name']}

    field_arg: str = params.pop('field', '')
    if not field_arg:
        fields = [SourceStudentTable]

        # trait = lambda student: student.to_dict()
        def trait(student: SourceStudentTable):
            return student.to_dict()
    else:
        columns: List[str] = field_arg.split(',')
        fields = [getattr(SourceStudentTable, column) for column in columns]

        # trait = lambda student: {k: getattr(student, k) for k in columns}
        def trait(student: SourceStudentTable):
            return {k: getattr(student, k) for k in columns}

    ids: List[str] = [s for s in params.pop('admission_id', '').split(',') if s]
    for idx, id_ in enumerate(ids):
        if id_.startswith('*'):
            id_ = '%' + id_[1:]
        if id_.endswith('*'):
            id_ = id_[:-1] + '%'
        ids[idx] = id_

    params = {k: v for (k, v) in params.items() if v}
    query: orm.query = engine.session.query(*fields).filter_by(**params)
    if ids:
        id_filter = or_(*(SourceStudentTable.admission_id.like(id_) for id_ in ids))
        query: orm.query = query.filter(id_filter)
    return Response(students=[trait(student) for student in query.all()]).json()
