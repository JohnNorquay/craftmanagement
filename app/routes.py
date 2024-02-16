from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models import User, CraftProject, Product
from app.forms import LoginForm, RegistrationForm, CraftProjectForm, ProductForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    form = CraftProjectForm()
    if form.validate_on_submit():
        project = CraftProject(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            user_id=current_user.id
        )
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('projects'))  # Adjust according to your actual route
    # If the form is not validated on submit, this part will still execute, rendering the form again
    return render_template('create_project.html', form=form)

@app.route('/projects')
@login_required
def projects():
    projects = CraftProject.query.filter_by(user_id=current_user.id).all()
    return render_template('projects.html', projects=projects)

@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = CraftProject.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        abort(403)
    form = CraftProjectForm(obj=project)
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        project.start_date = form.start_date.data
        project.end_date = form.end_date.data
        db.session.commit()
        flash('Your project has been updated!', 'success')
        return redirect(url_for('projects'))
    return render_template('edit_project.html', title='Edit Project', form=form, legend='Edit Project')

@app.route("/delete_project/<int:project_id>", methods=['POST'])
@login_required
def delete_project(project_id):
    project = CraftProject.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    flash('Your project has been deleted!', 'success')
    return redirect(url_for('projects'))

@app.route("/project/<int:project_id>/add_product", methods=['GET', 'POST'])
@login_required
def add_product(project_id):
    project = CraftProject.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        # Ensuring that only the project owner can add products
        abort(403)

    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data,
                          quantity=form.quantity.data,
                          price=form.price.data if form.price.data else None,  # Handling optional price
                          status=form.status.data,
                          project_id=project_id)
        db.session.add(product)
        db.session.commit()
        flash('Product added to project!', 'success')
        return redirect(url_for('project_details'))  # Redirect to the list of projects
    return render_template('add_product.html', title='Add Product', form=form, project=project)

@app.route("/project/<int:project_id>")
@login_required
def project_details(project_id):
    project = CraftProject.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        abort(403)
    products = Product.query.filter_by(project_id=project.id).all()
    return render_template('project_details.html', project=project, products=products)



