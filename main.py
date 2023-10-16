from flask import Blueprint,render_template,Flask,redirect,url_for,request,flash
from flask_login import login_required,current_user
from models import Workout,User
from init import db

# initialize main file as a part of flask application
main=Blueprint('main',__name__)

# Angela always called this app.route and I did'nt know why, well i called it main.route because the app is called main, and this is the decorator function
@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',name=current_user.name)

@main.route('/new')
def new_workout():
    return render_template('create_workout.html')

@main.route('/new',methods=['POST'])
def new_workout_post():
    number= request.form.get('pushups')
    comment= request.form.get('comment')
    new_workout= Workout(pushups=number,comment=comment,author=current_user)
    db.session.add(new_workout)
    db.session.commit()
    flash('Your workout has been added')
    return redirect(url_for('main.user_workouts'))

@main.route('/all')
@login_required
def user_workouts():
    page=request.args.get('page',1,type=int)
    user=User.query.filter_by(email=current_user.email).first_or_404()
    # so i want to introduce paginatio so users would not have to scroll so much.
    # workouts=user.workouts
    workouts=Workout.query.filter_by(author=user).paginate(page=page,per_page=5)
    return render_template('all_workouts.html',workouts=workouts,user=user)


@main.route('/delete/<int:workout_id>')
@login_required
def delete(workout_id):
    workout_to_delete=Workout.query.get_or_404(workout_id)
    db.session.delete(workout_to_delete)
    db.session.commit()
    return redirect(url_for('main.user_workouts'))


@main.route('/edit/<int:workout_id>',methods=['GET','POST'])
@login_required
def update_workout(workout_id):
    workout_to_edit=Workout.query.get_or_404(workout_id)
    if request.method=='POST':
        # why is the syntax her different
        workout_to_edit.pushups=request.form['pushups']
        workout_to_edit.comment = request.form['comment']
        db.session.commit()
        flash('Your workout has been updated')
        return redirect(url_for('main.user_workouts'))
    return render_template('update_workout.html',workout=workout_to_edit)