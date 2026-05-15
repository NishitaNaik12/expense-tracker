from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import Expense, User
from datetime import datetime, date

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    category_filter = request.args.get('category')
    sort_by = request.args.get('sort', 'date_desc')
    
    # Filter by current_user.id
    query = Expense.query.filter_by(user_id=current_user.id)
    
    if category_filter:
        query = query.filter(Expense.category == category_filter)
        
    if sort_by == 'amount_asc':
        query = query.order_by(Expense.amount.asc())
    elif sort_by == 'amount_desc':
        query = query.order_by(Expense.amount.desc())
    else: # Default to date_desc
        query = query.order_by(Expense.spent_on.desc())
        
    expenses = query.all()
    total_amount = sum(e.amount for e in expenses)
    
    grouped_expenses = []
    current_month = None
    
    if sort_by == 'date_desc':
        for expense in expenses:
            month_name = expense.spent_on.strftime('%B %Y')
            if month_name != current_month:
                grouped_expenses.append({'month': month_name, 'expenses': [], 'total': 0})
                current_month = month_name
            grouped_expenses[-1]['expenses'].append(expense)
            grouped_expenses[-1]['total'] += expense.amount
    else:
        grouped_expenses = [{
            'month': 'Sorted by Amount' if not category_filter else f'Filtered: {category_filter}',
            'expenses': expenses,
            'total': total_amount
        }]
            
    return render_template('index.html', groups=grouped_expenses, total_amount=total_amount, 
                           current_category=category_filter, current_sort=sort_by)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('main.register'))
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('login.html')

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        spent_on = datetime.strptime(request.form.get('spent_on'), '%Y-%m-%d').date()

        new_expense = Expense(
            title=title,
            description=description,
            amount=amount,
            category=category,
            spent_on=spent_on,
            user_id=current_user.id
        )
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!')
        return redirect(url_for('main.index'))
    
    return render_template('expense_form.html', action="Add", today=date.today())

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    # Ensure isolation: filter by id AND current_user.id
    expense = Expense.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        expense.title = request.form.get('title')
        expense.description = request.form.get('description')
        expense.amount = float(request.form.get('amount'))
        expense.category = request.form.get('category')
        expense.spent_on = datetime.strptime(request.form.get('spent_on'), '%Y-%m-%d').date()

        db.session.commit()
        flash('Expense updated successfully!')
        return redirect(url_for('main.index'))
    
    return render_template('expense_form.html', expense=expense, action="Edit")

@main.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_expense(id):
    # Ensure isolation: filter by id AND current_user.id
    expense = Expense.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!')
    return redirect(url_for('main.index'))
