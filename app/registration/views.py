from flask import render_template, redirect, url_for, flash
from . import registration_blueprint
from app.db import db
from .models import Uni
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from app.user import groups_required

from . import api

class UniForm(FlaskForm):
    name = StringField('Uni Name')
    token = StringField('Token')
    submit = SubmitField()

@registration_blueprint.route('/admin/uni')
@groups_required('admin')
def unis():
    unis = Uni.query.all()
    return render_template('admin/unis.html', unis = unis)

@registration_blueprint.route('/admin/uni/new', methods=['GET', 'POST'])
@groups_required('admin')
def add_uni():
    form = UniForm()
    if form.validate_on_submit():
        uni = Uni(form.name.data, form.token.data)
        db.session.add(uni)
        try:
            db.session.commit()
        except IntegrityError as e:
            if 'uni.name' in str(e.orig):
                form.name.errors.append("There is already a uni with that name")
            elif 'uni.token' in str(e.orig):
                form.token.errors.append("There is already a uni with that token")
            else:
                raise
            return render_template('admin/uniform.html', form = form)
        return redirect(url_for('registration.unis'))
    return render_template('admin/uniform.html', form = form)

@registration_blueprint.route('/admin/uni/<int:uni_id>/delete')
@groups_required('admin')
def delete_uni(uni_id):
    uni = Uni.query.filter_by(id=uni_id).first()
    flash('Deleted {uni.name}'.format(uni=uni))
    db.session.delete(uni)
    db.session.commit()
    return redirect(url_for('registration.unis'))

@registration_blueprint.route('/admin/uni/<int:uni_id>/edit', methods=['GET', 'POST'])
@groups_required('admin')
def edit_uni(uni_id):
    uni = Uni.query.filter_by(id=uni_id).first()
    form = UniForm(name = uni.name, token = uni.token)
    if form.validate_on_submit():
        from sqlalchemy.exc import IntegrityError
        uni = Uni(form.name.data, form.token.data)
        db.session.add(uni)
        try:
            db.session.commit()
        except IntegrityError as e:
            if 'uni.name' in str(e.orig):
                form.name.errors.append("There is already a uni with that name")
            elif 'uni.token' in str(e.orig):
                form.token.errors.append("There is already a uni with that token")
            else:
                raise
            return render_template('admin/uniform.html', form = form)
        return redirect(url_for('registration.unis'))
    return render_template('admin/uniform.html', form = form)
