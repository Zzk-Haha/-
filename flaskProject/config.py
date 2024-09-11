

SECRET_KEY = 'asdasdsa;fa'
#数据库的配置信息
HOSTNAME='127.0.0.1'
PORT='3306'
DATABASE='zuozuokan'
USERNAME='root'
PASSWORD='admin'
DB_URI='mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI=DB_URI


# 邮箱配置
MAIL_SERVER='smtp.qq.com'
MAIL_USE_SSL=True
# 邮箱端口
MAIL_PORT='465'
# 邮箱账号
MAIL_USERNAME='2074217155@qq.com'
# 授权码
MAIL_PASSWORD='fehdmlgahedgedcg'
# 邮箱账号
MAIL_DEFAULT_SENDER='2074217155@qq.com'