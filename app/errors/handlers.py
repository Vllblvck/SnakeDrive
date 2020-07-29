from flask import render_template, request

from app import db
from app.errors import bp
from app.api.errors import error_response


@bp.errorhandler(404)
def not_found_error(error):
    return error_response(404)


@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return error_response(500)
