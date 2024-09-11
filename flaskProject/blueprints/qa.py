
from flask import Blueprint,request
from flask import render_template, redirect, url_for,g
from .forms import QuestionForm,AnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from decorators import login_required
bp=Blueprint('qa',__name__,url_prefix='/')

@bp.route('/')
def home():
    return render_template("home.html")

# http://127.0.0.1:5000
@bp.route('/index')
@login_required
def index():
    questions=QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('index.html',questions=questions)

@bp.route('qa/public',methods=['GET','POST'])
# 装饰器
@login_required
def public_question():
    if request.method == 'GET':
        return render_template('public_question.html')
    else:
        form=QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title,content=content,author=g.user)
            db.session.add(question)
            db.session.commit()
            # 跳转到详情页
            return redirect(url_for('qa.index'))
        else:
            print(form.errors)
            return redirect(url_for('qa.public_question'))

@bp.route('qa/detail/<qa_id>')
def qa_detail(qa_id):
    question=QuestionModel.query.get(qa_id)
    return render_template('detail.html',question=question)

# @bp.route('/answer/public',methods=['POST'])
@bp.post('/answer/public')
@login_required
def  public_answer():
    form=AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(question_id=question_id,content=content,author_id=g.user.id)

        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('qa.qa_detail',qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for('qa.qa_detail',qa_id=request.form.get('question_id')))

@bp.route('/lanxin')
def lanxin():
    return render_template('lanxin.html')




@bp.route('/search')
def search():
    # /search?q=flask
    # /search/<q>
    # post ,request.form
    q=request.args.get('q')
    questions=QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template('index.html',questions=questions)


@bp.route('/xunfei')
def xunfei():
    return render_template('xunfei.html')

