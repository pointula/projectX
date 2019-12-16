from flask import Blueprint, render_template

main = Blueprint('main',__name__)


@main.route('/')
def index():
    return render_template('index.html', title=f'Home page - Pointula')

@main.route('/home-page/terms-and-condition')
def terms_and_condition():
    return render_template('terms.html', title=f'Pointula Terms and condition')

@main.route('/home-page/faq')
def faq():
    return render_template('faq.html', title=f'Pointula FAQs')