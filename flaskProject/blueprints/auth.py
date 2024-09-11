import time
from flask import Blueprint,render_template,jsonify,redirect,url_for,session,request
from exts import mail,db
from flask_mail import Message
from flask import request
import string
import random
from models import  EmailCaptchaModel
from .forms import RegisterForm,LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash,check_password_hash
# /auth
bp=Blueprint("auth",__name__,url_prefix='/auth')

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form=LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user=UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在！")
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password,password):
                # cookie中不适合存储太多的数据，只适合少量的数据
                # 一般用来存放登录授权的东西
                # flask中的seeion是经过加密后存储在cookie中的
                session["user_id"]=user.id
                return redirect(url_for('qa.index'))
            else:
                print('密码错误!')
                return redirect(url_for('auth.login'))

        else:
            print(form.errors)
            return redirect(url_for('auth.login'))



@bp.route('/detail')
def detail():
    return render_template('detail.html')



@bp.route('/predict', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        # 处理上传的文件和进行预测

        # prediction 是预测结果
        prediction = '根据CT影像特征提取分析，该患者的肺部密度值偏高，肺部纹理粗糙且紊乱，这表明肺部受到了炎症或感染的影响。此外，患者的肺部体积缩小，这可能是由于肺部组织受到压迫或破坏导致的。这些影像特征通常与重症肺炎、肺结核、肺癌等疾病相关。进一步观察发现，患者的肺部边缘模糊，与周围组织的界限不清，这可能是由于肺部水肿或炎症引起的。同时，患者的肺部有多个空洞或气囊形成，这可能是由于肺部组织坏死或空洞性病变导致的。此外，患者的肺部有明显的血管扩张和扭曲，这可能是由于肺部血管受到炎症或感染的影响导致的。综上所述，根据CT影像特征提取分析，该患者的影像特征与重症患者相符，很可能是重症肺炎、肺结核、肺癌等疾病。建议尽快进行进一步的检查和治疗，以明确诊断并采取相应的治疗措施。'
        # 返回一个 JSON 响应
        return jsonify({'result': prediction})
    else:
        # 返回 HTML 页面
        return render_template('prediction.html')


@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    # 验证用户提交的邮箱和验证码是否正确
    # 表单验证：flask-wtf：wtforms
    else:
        form=RegisterForm(request.form)
        if form.validate():
            email=form.email.data
            username=form.username.data
            password=form.password.data
            user=UserModel(email=email,username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.register'))

@bp.route('/logout')
def logout():
    # 清除session信息
    session.clear()
    return redirect('/')


#bp.route,如果没有指定methods参数，默认是get请求
#@bp.route('/captcha/email',methods=['POST'])
@bp.route('/captcha/email')
def gety_captcha():
    email=request.args.get('email')
    # 4/6位随机数字或字母的组合
    source=string.digits*6+string.ascii_lowercase
    captcha=random.sample(source,6)
    # print(captcha)
    captcha=''.join(captcha)
    message = Message(subject='注册验证码', recipients=[email], body=f'您的验证码是:{captcha},收到验证码后仅个人使用,不可提供他人使用!')
    mail.send(message)
    # 用数据库方式存储
    email_captcha=EmailCaptchaModel(email=email,captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({'code':200,'message':'','data':None})


@bp.route('/mail/test')
def mail_test():
    message=Message (subject='邮件测试',recipients=['3255456932@qq.com'],body='this is a test')
    mail.send(message)
    return "邮件发送成功!"

