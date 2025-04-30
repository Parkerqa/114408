import self,jwt, MySQLdb,MySQLdb.cursors,datetime
from flask import Flask, request, redirect, url_for, flash, jsonify,current_app
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from MySQLdb.cursors import DictCursor
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer
import string , random ,os, uuid
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import  timedelta
from functools import wraps


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 設定 MySQL 連線資訊
app.config['MYSQL_HOST'] = '140.131.114.242'
app.config['MYSQL_USER'] = '114408TTS'
app.config['MYSQL_PASSWORD'] = 'xD11u3siew*rzRn'
app.config['MYSQL_DB'] = '114-408'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 未登入時，導向的頁面
app.secret_key = 'your_secret_key'  # 保持 session 安全
SECRET_KEY = 'your_secret_key'
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
bcrypt = Bcrypt()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_reset_token(email):
    return s.dumps(email, salt='password-reset-salt')

def confirm_reset_token(token, expiration=3600):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=expiration)
        return email
    except Exception as e:
        return None

def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def generate_auth_token(uid):
    payload = {
        'uid': uid,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token 缺失'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = data  # 保存用戶資料在 request 上
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token 過期'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': '無效的 Token'}), 401

        return f(*args, **kwargs)
    return decorated

class User(UserMixin):
    def __init__(self, uid, username, priority):
        self.id = uid  # Flask-Login 預設要有 .id 屬性
        self.username = username
        self.priority = priority

# 加載使用者
@login_manager.user_loader
def load_user(user_uid):
    from MySQLdb.cursors import DictCursor
    with app.app_context():  # 只有在你確定不是在請求處理流程時才需要這行
        cur = mysql.connection.cursor(DictCursor)
        cur.execute("SELECT uid, username, priority FROM User WHERE uid = %s", (user_uid,))
        user_data = cur.fetchone()
        cur.close()

    if user_data:
        return User(user_data['uid'], user_data['username'], user_data['priority'])
    return None

# 註冊功能
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if request.method == 'POST':
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        print(username, email, password, hashed_pw)
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO User (username, password, email, priority) VALUES (%s, %s, %s, %s)",
                        (username, hashed_pw, email, 0))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': '註冊成功！', 'state': 'success'})
        except Exception as e:
            return jsonify({'message': '註冊失敗', 'state': 'error'}), 404

# 登入功能
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM User WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        token = jwt.encode({
            'uid': user['uid'],
            'username': user['username'],
            'priority': user['priority'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({'message': '登入成功', 'state': 'success','token': token})

    return jsonify({'message': '信箱或密碼錯誤', 'state': 'error'})

# 重設密碼
@app.route('/forget_password', methods=['POST'])
def forget_password():
    data = request.json
    email = data.get('email')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM User WHERE email = %s", (email,))
    user = cur.fetchone()

    if user:
        new_password = generate_random_password()
        hashed_pw = bcrypt.generate_password_hash(new_password).decode('utf-8')

        cur.execute("UPDATE User SET password = %s WHERE email = %s", (hashed_pw, email))
        mysql.connection.commit()
        cur.close()

        print(f"📧 已寄送新密碼到 {email}")
        print(f"🔐 新密碼是：{new_password}")

        return jsonify({'message': '我們已幫您重設密碼，請查看信箱', 'state': 'success'})

    cur.close()
    return jsonify({'message': '找不到此 email','state': 'error'}), 404

# 修改使用者
@app.route('/change_user_if', methods=['PATCH'])
@token_required
def change_user_if():
    try:
        data = request.get_json()
        new_username = data.get('username')
        new_email = data.get('email')
        new_password = data.get('new_password')
        old_password = data.get('old_password')

        if new_password and not old_password:
            return jsonify({'message': '舊密碼為必填項目','state': 'error'}), 400

        cur = mysql.connection.cursor()

        # 查詢當前用戶的密碼
        cur.execute("SELECT password FROM User WHERE uid = %s", (current_user.get_id(),))
        stored_pw = cur.fetchone()

        if stored_pw is None:
            return jsonify({'message': '找不到用戶資料','state': 'error'}), 404

        if new_password:
            # 核對舊密碼是否正確
            if not bcrypt.check_password_hash(stored_pw['password'], old_password):
                return jsonify({'message': '舊密碼錯誤','state': 'error'}), 400

            # 加密新密碼
            hashed_new = bcrypt.generate_password_hash(new_password).decode('utf-8')
            cur.execute("UPDATE User SET password = %s WHERE uid = %s", (hashed_new, current_user.get_id()))

        # 更新用戶名
        if new_username:
            cur.execute("UPDATE User SET username = %s WHERE uid = %s", (new_username, current_user.get_id()))

        # 更新用戶郵箱
        if new_email:
            cur.execute("UPDATE User SET email = %s WHERE uid = %s", (new_email, current_user.get_id()))

        mysql.connection.commit()
        cur.close()

        return jsonify({'message': '資料更新成功','state': 'success'}), 200

    except Exception as e:
        print(f"[ERROR] 更新資料錯誤：{e}")
        return jsonify({'message': '更新資料時發生錯誤', 'state': 'error'}), 500



# 查詢發票
@app.route('/list_ticket', methods=['GET'])
@token_required
def list_ticket():
    try:
        cur = mysql.connection.cursor()

        if current_user.priority == 1:
            cur.execute("""
                SELECT T.tid, T.declaration_date, T.type, T.status,
                       TD.title, TD.money
                FROM Ticket T
                LEFT JOIN Ticket_detail TD ON T.tid = TD.tid
            """)
        else:
            cur.execute("""
                SELECT T.tid, T.declaration_date, T.type, T.status,
                       TD.title, TD.money
                FROM Ticket T
                LEFT JOIN Ticket_detail TD ON T.tid = TD.tid
                WHERE T.uid = %s
            """, (current_user.id,))

        tickets = cur.fetchall()
        cur.close()
        if not tickets:
            return jsonify({'message': '目前沒有發票資料','state':'error'}), 404

        results = []
        for t in tickets:
            results.append({
                '編號': t['tid'],
                '報帳時間': t['declaration_date'],
                '報帳種類': t['type'],
                '標題': t['title'],
                '金額': t['money'],
                '狀態': t['status']
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({'message': '伺服器錯誤', 'state': 'error'}), 500

# 刪除發票
@app.route('/delete_ticket/<int:tid>', methods=['DELETE'])
@token_required
def delete_ticket(tid):
    try:
        cur = mysql.connection.cursor()

        # 查詢該發票
        cur.execute("SELECT * FROM Ticket WHERE tid = %s", (tid,))
        ticket = cur.fetchone()

        if not ticket:
            return jsonify({'message': '找不到該發票','state': 'error'}), 404

        # 所有人都不能刪除 status 為 2 的發票
        if ticket['status'] == 2:
            return jsonify({'message': '無法刪除已完成的發票','state': 'error'}), 403

        # 一般使用者只能刪除自己的發票
        if current_user.priority == 0 and ticket['uid'] != int(current_user.id):
            return jsonify({'message': '你無權刪除此發票','state': 'error'}), 403

        # 執行刪除
        cur.execute("DELETE FROM Ticket_detail WHERE tid = %s", (tid,))
        cur.execute("DELETE FROM Ticket WHERE tid = %s", (tid,))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': '發票已成功刪除','state': 'success'}), 200

    except Exception as e:
        return jsonify({'message': '刪除發票時發生錯誤', 'state': 'error'}), 500

#修改發票內容
@app.route('/change_ticket/<int:tid>', methods=['PATCH'])
@token_required
def change_ticket(tid):
    try:
        data = request.get_json()
        new_class = data.get('class')
        new_details = data.get('detail')

        if not new_class or not isinstance(new_details, list):
            return jsonify({'message': '請提供 class 和 detail','state': 'error'}), 400

        cur = mysql.connection.cursor()

        # 查詢 Ticket
        cur.execute("SELECT * FROM Ticket WHERE tid = %s", (tid,))
        ticket = cur.fetchone()
        if not ticket:
            return jsonify({'message': '找不到發票', 'state': 'error'}), 404

        if int(ticket['status']) == 2:
            return jsonify({'message': '無法修改已完成的發票', 'state': 'error'}), 403

        if current_user.priority == 0 and ticket['uid'] != int(current_user.id):
            return jsonify({'message': '你無權修改這張發票', 'state': 'error'}), 403

        # 更新 class
        cur.execute("UPDATE Ticket SET class = %s WHERE tid = %s", (new_class, tid))

        # 查出目前的 detail id 列表
        cur.execute("SELECT td_id FROM Ticket_detail WHERE td_id = %s", (tid,))
        existing_detail_ids = {row['id'] for row in cur.fetchall()}

        new_detail_ids = set()
        for item in new_details:
            title = item.get('title')
            money = item.get('money')

            if title is None or money is None:
                continue

            if 'id' in item:
                detail_id = item['id']
                new_detail_ids.add(detail_id)

                if detail_id in existing_detail_ids:
                    cur.execute(
                        "UPDATE Ticket_detail SET title = %s, money = %s WHERE id = %s AND td_id = %s",
                        (title, money, detail_id, tid)
                    )
                else:
                    return jsonify({'message': f'找不到明細 id {detail_id}','state':'error'}), 400
            else:
                # 新增明細
                cur.execute(
                    "INSERT INTO Ticket_detail (title, money) VALUES (%s, %s)",
                    (title, money)
                )

        # 刪除被移除的明細
        ids_to_delete = existing_detail_ids - new_detail_ids
        if ids_to_delete:
            cur.execute(
                f"DELETE FROM Ticket_detail WHERE id IN ({','.join(['%s'] * len(ids_to_delete))})",
                tuple(ids_to_delete)
            )

        mysql.connection.commit()
        cur.close()

        return jsonify({'message': '發票已成功修改','state': 'success'}), 200

    except Exception as e:
        print(f"[ERROR] 修改發票錯誤：{e}")
        return jsonify({'message': '修改發票時發生錯誤', 'state': 'error'}), 500

#查詢發票內容
@app.route('/search_ticket', methods=['GET'])
@token_required
def search_ticket():
    try:
        keyword = request.args.get('q', '').strip()

        if not keyword:
            return jsonify({'message': '請提供查詢字詞參數 q', 'state': 'error'}), 400

        cur = mysql.connection.cursor(DictCursor)

        # 查詢語句
        query = """
            SELECT T.*, TD.title, TD.money
            FROM Ticket T
            LEFT JOIN Ticket_detail TD ON T.tid = TD.td_id
            WHERE T.creatdate LIKE %s
               OR T.class LIKE %s
               OR T.invoice_number LIKE %s
               OR TD.title LIKE %s
               OR CAST(TD.money AS CHAR) LIKE %s
        """

        like_keyword = f"%{keyword}%"
        cur.execute(query, (like_keyword, like_keyword, like_keyword, like_keyword, like_keyword))
        results = cur.fetchall()
        cur.close()

        # 權限過濾：一般使用者只看部分欄位
        if current_user.priority == 0:
            filtered_results = []
            for row in results:
                filtered_results.append({
                    'class': row.get('class'),
                    'ticket_create': row.get('ticket_create'),
                    'invoice_number': row.get('invoice_number'),
                    'title': row.get('title'),
                    'money': row.get('money')
                })
            return jsonify({'results': filtered_results}), 200

        # 管理員 → 顯示全部
        return jsonify({'results': results}), 200

    except Exception as e:
        print(f"[ERROR] 查詢發票錯誤：{e}")
        return jsonify({'message': '查詢時發生錯誤','state': 'error'}), 500

#上傳發票
@app.route('/upload', methods=['POST'])
@token_required
def upload():
    if 'photo' not in request.files:
        return jsonify({'message': '缺少 photo', 'state': 'error'}), 400

    file = request.files['photo']

    if not file or file.filename == '':
        return jsonify({'message': '未選擇檔案', 'state': 'error'}), 400

    if not allowed_file(file.filename):
        return jsonify({'message': '不支援的檔案格式', 'state': 'error'}), 400

    try:
        ext = file.filename.rsplit('.', 1)[1].lower()
        new_filename = f"{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(save_path)

        # 建立新的發票，並記錄圖片檔名
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Ticket (uid, img, status) VALUES (%s, %s, %s)", (current_user.id, new_filename, 0))
        tid = cur.lastrowid  # 取得剛剛新增的 tid
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': '圖片上傳並建立新發票成功','state':'success', 'filename': new_filename, 'tid': tid}), 200

    except Exception as e:
        print(f"[ERROR] 上傳圖片失敗：{e}")
        return jsonify({'message': '伺服器錯誤','state': 'error'}), 500

#總結金額
@app.route('/total_money', methods=['GET'])
@token_required
def total_money():
    try:
        cur = mysql.connection.cursor(DictCursor)

        # 執行加總查詢
        cur.execute("SELECT SUM(money) AS total_money FROM Ticket_detail")
        result = cur.fetchone()
        cur.close()

        total = result['total_money'] if result['total_money'] is not None else 0

        return jsonify({'total_money': total}), 200

    except Exception as e:
        print(f"[ERROR] 加總 money 失敗：{e}")
        return jsonify({'message': '加總時發生錯誤','state': 'error'}), 500

#用種類查詢發票
@app.route('/list_type', methods=['GET'])
@token_required
def list_type():
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT DISTINCT class FROM Ticket")
    classes = [row['class'] for row in cur.fetchall()]
    cur.close()

    return jsonify({'classes': classes}), 200

#用日期查詢發票
@app.route('/list_date', methods=['GET'])
@token_required
def list_date():
    cur = mysql.connection.cursor()
    # 使用 DATE_FORMAT 將 creatdate 格式化為 yyyy/mm/dd
    cur.execute("SELECT DISTINCT DATE_FORMAT(creatdate, '%Y/%m/%d') AS formatted_date FROM Ticket")
    dates = [row['formatted_date'] for row in cur.fetchall()]
    cur.close()

    return jsonify({'dates': dates}), 200

# 登出
@app.route('/logout', methods=['POST'])
@token_required
def logout():
    logout_user()
    return jsonify({'message': '登出成功','state': 'success'}), 200

#上傳使用者照片
@app.route('/upload_user_photo', methods=['POST'])
@token_required
def upload_user_photo():
    if 'photo' not in request.files:
        return jsonify({'message': '缺少 photo', 'state': 'error'}), 400

    file = request.files['photo']

    if not file or file.filename == '':
        return jsonify({'message': '未選擇檔案','state': 'error'}), 400

    if not allowed_file(file.filename):
        return jsonify({'message': '不支援的檔案格式', 'state': 'error'}), 400

    try:
        ext = file.filename.rsplit('.', 1)[1].lower()
        new_filename = f"{uuid.uuid4().hex}.{ext}"

        # 確保 user_photo 資料夾存在
        upload_folder = os.path.join(current_app.root_path, 'user_photo')
        os.makedirs(upload_folder, exist_ok=True)

        save_path = os.path.join(upload_folder, new_filename)
        file.save(save_path)

        # 查詢舊的大頭貼檔名
        cur = mysql.connection.cursor()
        cur.execute("SELECT img FROM User WHERE uid = %s", (current_user.id,))
        old_photo = cur.fetchone()

        # 更新新的圖片到資料庫
        cur.execute("UPDATE User SET img = %s WHERE uid = %s", (new_filename, current_user.id))
        mysql.connection.commit()
        cur.close()

        # 刪除舊的大頭貼檔案（如果存在且不是空值）
        if old_photo and old_photo['img']:
            old_path = os.path.join(upload_folder, old_photo['img'])
            if os.path.exists(old_path):
                os.remove(old_path)

        return jsonify({'message': '大頭貼上傳成功','state' : 'success' ,'filename': new_filename}), 200

    except Exception as e:
        print(f"[ERROR] 上傳大頭貼失敗：{e}")
        return jsonify({'message': '伺服器錯誤', 'state': 'error'}), 500

#修改黑白模式
@app.route('/change_theme', methods=['PATCH'])
@token_required
def change_theme():
    try:
        data = request.get_json()
        new_theme = data.get('theme')


        cur = mysql.connection.cursor()

        # 查詢 othersetting 是否已有資料
        cur.execute("SELECT theme FROM othersetting WHERE uid = %s", (current_user.id,))
        setting = cur.fetchone()

        if setting:
            # 有找到，直接更新
            cur.execute("UPDATE othersetting SET theme = %s WHERE uid = %s", (new_theme, current_user.id))
        else:
            # 沒找到，新增一筆資料
            cur.execute("INSERT INTO othersetting (uid, theme) VALUES (%s, %s)", (current_user.id, new_theme))

        mysql.connection.commit()
        cur.close()

        return jsonify({'message': '主題模式已更新','state' : 'success' ,'theme': new_theme}), 200

    except Exception as e:
        print(f"[ERROR] 修改主題模式失敗：{e}")
        return jsonify({'message': '伺服器錯誤','state': 'error'}), 500

#使用者列表
@app.route('/list_user', methods=['GET'])
@token_required
def list_user():
    try:
        # 直接設定 DictCursor
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username, email FROM User WHERE uid = %s", (current_user.id,))
        user = cur.fetchone()
        cur.close()

        if not user:
            return jsonify({'message': '找不到使用者', 'state': 'error'}), 404

        user_info = {
            'username': user['username'],
            'email': user['email']
        }

        return jsonify({'user': user_info}), 200

    except Exception as e:
        print(f"[ERROR] 取得當前使用者資料失敗：{e}")
        return jsonify({'message': '伺服器錯誤', 'state': 'error'}), 500


#統計未審核的發票
@app.route('/unaudited_invoices', methods=['GET'])
@token_required
def unaudited_invoices():
    try:
        cur = mysql.connection.cursor()

        # 查詢所有 status = 1 的票券數量
        cur.execute("SELECT COUNT(*) AS count FROM Ticket WHERE status = 1")
        result = cur.fetchone()

        cur.close()

        return jsonify({'message': '統計成功','state': 'success','status_1_count': result['count']}), 200

    except Exception as e:
        print(f"[ERROR] 統計 status=1 錯誤：{e}")
        return jsonify({'message': '統計失敗','state': 'error'}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)