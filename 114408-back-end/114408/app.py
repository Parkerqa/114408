import self,jwt,MySQLdb.cursors,datetime
from flask import Flask, request, redirect, url_for, flash, jsonify,current_app,g
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
        'exp': datetime.utcnow() + timedelta(days=2)
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
            g.user = data
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
    with app.app_context():
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

#驗證token
@app.route('/verify', methods=['GET'])
def verify():
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

    if not token:
        return jsonify({'message': 'Token 缺失', 'state': 'error'}), 401

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'message': 'Token 有效', 'state': 'success', 'data': data}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token 已過期', 'state': 'error'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': '無效的 Token', 'state': 'error'}), 401

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

        uid = g.user['uid']  # 從 token 中取得 uid
        cur = mysql.connection.cursor()

        # 查詢當前用戶的密碼
        cur.execute("SELECT password FROM User WHERE uid = %s", (uid,))
        stored_pw = cur.fetchone()

        if stored_pw is None:
            return jsonify({'message': '找不到用戶資料','state': 'error'}), 404

        if new_password:
            # 核對舊密碼是否正確
            if not bcrypt.check_password_hash(stored_pw['password'], old_password):
                return jsonify({'message': '舊密碼錯誤','state': 'error'}), 400

            # 加密新密碼
            hashed_new = bcrypt.generate_password_hash(new_password).decode('utf-8')
            cur.execute("UPDATE User SET password = %s WHERE uid = %s", (hashed_new, uid))

        # 更新用戶名
        if new_username:
            cur.execute("UPDATE User SET username = %s WHERE uid = %s", (new_username, uid))

        # 更新用戶郵箱
        if new_email:
            cur.execute("UPDATE User SET email = %s WHERE uid = %s", (new_email, uid))

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
        uid = g.user['uid']
        priority = g.user['priority']

        cur = mysql.connection.cursor()

        if priority == 1:
            # 管理員查全部
            cur.execute("""
                SELECT T.tid, T.creatdate, T.type, T.status,
                       TD.title, TD.money, T.uid, T.check_man, T.writeoff_date
                FROM Ticket T
                LEFT JOIN Ticket_detail TD ON T.tid = TD.tid
            """)
        else:
            # 一般使用者查自己
            cur.execute("""
                SELECT T.invoice_number, T.creatdate, T.type, T.status,
                       TD.title, TD.money
                FROM Ticket T
                LEFT JOIN Ticket_detail TD ON T.tid = TD.tid
                WHERE T.uid = %s
            """, (uid,))

        tickets = cur.fetchall()
        cur.close()

        if not tickets:
            return jsonify({'message': '目前沒有發票資料', 'state': 'error'}), 404

        results = [{
            'time': t['creatdate'],
            'type': t['type'],
            'title': t['title'],
            'money': t['money'],
            'state': t['status'],
            'number': t['invoice_number'],
        } for t in tickets]

        return jsonify({'message': '成功', 'state': 'success', 'data': results})

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
            return jsonify({'message': '找不到該發票', 'state': 'error'}), 404

        # 所有人都不能刪除 status 為 2 的發票
        if ticket['status'] == 2:
            return jsonify({'message': '無法刪除已完成的發票', 'state': 'error'}), 403

        # 一般使用者只能刪除自己的發票
        if g.user['priority'] == 0 and ticket['uid'] != g.user['uid']:
            return jsonify({'message': '你無權刪除此發票', 'state': 'error'}), 403

        # 執行刪除
        cur.execute("DELETE FROM Ticket_detail WHERE tid = %s", (tid,))
        cur.execute("DELETE FROM Ticket WHERE tid = %s", (tid,))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': '發票已成功刪除', 'state': 'success'}), 200

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
            return jsonify({'message': '請提供 class 和 detail', 'state': 'error'}), 400

        cur = mysql.connection.cursor()

        # 查詢 Ticket
        cur.execute("SELECT * FROM Ticket WHERE tid = %s", (tid,))
        ticket = cur.fetchone()
        if not ticket:
            return jsonify({'message': '找不到發票', 'state': 'error'}), 404

        if int(ticket['status']) == 2:
            return jsonify({'message': '無法修改已完成的發票', 'state': 'error'}), 403

        if g.user['priority'] == 0 and ticket['uid'] != g.user['uid']:
            return jsonify({'message': '你無權修改這張發票', 'state': 'error'}), 403

        # 更新 class
        cur.execute("UPDATE Ticket SET class = %s WHERE tid = %s", (new_class, tid))

        # 查出目前的明細 id 列表
        cur.execute("SELECT td_id FROM Ticket_detail WHERE tid = %s", (tid,))
        existing_detail_ids = {row['td_id'] for row in cur.fetchall()}

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
                        "UPDATE Ticket_detail SET title = %s, money = %s WHERE td_id = %s AND tid = %s",
                        (title, money, detail_id, tid)
                    )
                else:
                    return jsonify({'message': f'找不到明細 id {detail_id}', 'state': 'error'}), 400
            else:
                # 新增明細
                cur.execute(
                    "INSERT INTO Ticket_detail (tid, title, money) VALUES (%s, %s, %s)",
                    (tid, title, money)
                )

        # 刪除被移除的明細
        ids_to_delete = existing_detail_ids - new_detail_ids
        if ids_to_delete:
            cur.execute(
                f"DELETE FROM Ticket_detail WHERE td_id IN ({','.join(['%s'] * len(ids_to_delete))})",
                tuple(ids_to_delete)
            )

        mysql.connection.commit()
        cur.close()

        return jsonify({'message': '發票已成功修改', 'state': 'success'}), 200

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

        # 修正 JOIN 條件：Ticket.tid 應對應 Ticket_detail.tid
        query = """
            SELECT T.*, TD.title, TD.money
            FROM Ticket T
            LEFT JOIN Ticket_detail TD ON T.tid = TD.tid
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

        # 權限過濾：一般使用者只能看自己的票且欄位有限
        if g.user['priority'] == 0:
            filtered_results = []
            for row in results:
                if row.get('uid') != g.user['uid']:
                    continue
                filtered_results.append({
                    'class': row.get('class'),
                    'ticket_create': row.get('creatdate'),  # 對應欄位修正
                    'invoice_number': row.get('invoice_number'),
                    'title': row.get('title'),
                    'money': row.get('money')
                })
            return jsonify({'results': filtered_results}), 200

        # 管理員 → 顯示全部欄位
        return jsonify({'results': results}), 200

    except Exception as e:
        print(f"[ERROR] 查詢發票錯誤：{e}")
        return jsonify({'message': '查詢時發生錯誤', 'state': 'error'}), 500

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
        cur.execute(
            "INSERT INTO Ticket (uid, img, status) VALUES (%s, %s, %s)",
            (g.user['uid'], new_filename, 0)
        )
        tid = cur.lastrowid  # 取得剛剛新增的 tid
        mysql.connection.commit()
        cur.close()

        return jsonify({
            'message': '圖片上傳並建立新發票成功',
            'state': 'success',
            'filename': new_filename,
            'tid': tid
        }), 200

    except Exception as e:
        print(f"[ERROR] 上傳圖片失敗：{e}")
        return jsonify({'message': '伺服器錯誤', 'state': 'error'}), 500

#總結金額
@app.route('/total_money', methods=['GET'])
@token_required
def total_money():
    try:
        cur = mysql.connection.cursor(DictCursor)

        if g.user['priority'] == 1:
            # 管理員：加總所有人金額
            cur.execute("SELECT SUM(money) AS total_money FROM Ticket_detail")
        else:
            # 一般用戶：只加總自己的發票金額
            cur.execute("""
                SELECT SUM(TD.money) AS total_money
                FROM Ticket_detail TD
                JOIN Ticket T ON TD.tid = T.tid
                WHERE T.uid = %s
            """, (g.user['uid'],))

        result = cur.fetchone()
        cur.close()

        total = result['total_money'] if result['total_money'] is not None else 0

        return jsonify({'total_money': total}), 200

    except Exception as e:
        print(f"[ERROR] 加總 money 失敗：{e}")
        return jsonify({'message': '加總時發生錯誤','state': 'error'}), 500

#用種類查詢發票
@app.route('/list_class', methods=['GET'])
@token_required
def list_class():
    try:
        cur = mysql.connection.cursor(DictCursor)

        # 查詢所有發票的類別
        cur.execute("SELECT DISTINCT class FROM Ticket")
        classes = [row['class'] for row in cur.fetchall()]
        cur.close()

        return jsonify({'classes': classes}), 200

    except Exception as e:
        print(f"[ERROR] 查詢類別失敗：{e}")
        return jsonify({'message': '查詢類別時發生錯誤', 'state': 'error'}), 500

#用日期查詢發票
@app.route('/list_date', methods=['GET'])
@token_required
def list_date():
    try:
        cur = mysql.connection.cursor()

        # 使用 DATE_FORMAT 將 creatdate 格式化為 yyyy/mm/dd
        cur.execute("SELECT DISTINCT DATE_FORMAT(creatdate, '%Y/%m/%d') AS formatted_date FROM Ticket")
        dates = [row['formatted_date'] for row in cur.fetchall()]
        cur.close()

        return jsonify({'dates': dates}), 200

    except Exception as e:
        print(f"[ERROR] 查詢日期失敗：{e}")
        return jsonify({'message': '查詢日期時發生錯誤', 'state': 'error'}), 500

# 登出
@app.route('/logout', methods=['POST'])
@token_required
def logout():
    try:
        # 清除 Token 中的用戶資料，登出
        logout_user()

        return jsonify({'message': '登出成功', 'state': 'success'}), 200
    except Exception as e:
        print(f"[ERROR] 登出錯誤：{e}")
        return jsonify({'message': '登出時發生錯誤', 'state': 'error'}), 500

#上傳使用者照片
@app.route('/upload_user_photo', methods=['POST'])
@token_required
def upload_user_photo():
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

        # 確保 user_photo 資料夾存在
        upload_folder = os.path.join(current_app.root_path, 'user_photo')
        os.makedirs(upload_folder, exist_ok=True)

        save_path = os.path.join(upload_folder, new_filename)
        file.save(save_path)

        # 查詢舊的大頭貼檔名
        cur = mysql.connection.cursor()
        cur.execute("SELECT img FROM User WHERE uid = %s", (g.user['uid'],))
        old_photo = cur.fetchone()

        # 更新新的圖片到資料庫
        cur.execute("UPDATE User SET img = %s WHERE uid = %s", (new_filename, g.user['uid']))
        mysql.connection.commit()
        cur.close()

        # 刪除舊的大頭貼檔案（如果存在且不是空值）
        if old_photo and old_photo['img']:
            old_path = os.path.join(upload_folder, old_photo['img'])
            if os.path.exists(old_path):
                os.remove(old_path)

        return jsonify({'message': '大頭貼上傳成功', 'state': 'success', 'filename': new_filename}), 200

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
        cur.execute("SELECT theme FROM othersetting WHERE uid = %s", (g.user['uid'],))
        setting = cur.fetchone()

        if setting:
            # 有找到，直接更新
            cur.execute("UPDATE othersetting SET theme = %s WHERE uid = %s", (new_theme, g.user['uid']))
        else:
            # 沒找到，新增一筆資料
            cur.execute("INSERT INTO othersetting (uid, theme) VALUES (%s, %s)", (g.user['uid'], new_theme))

        mysql.connection.commit()
        cur.close()

        return jsonify({'message': '主題模式已更新', 'state': 'success', 'theme': new_theme}), 200

    except Exception as e:
        print(f"[ERROR] 修改主題模式失敗：{e}")
        return jsonify({'message': '伺服器錯誤', 'state': 'error'}), 500

#使用者列表
@app.route('/list_user', methods=['GET'])
@token_required
def list_user():
    try:
        # 直接設定 DictCursor
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username, email FROM User WHERE uid = %s", (g.user['uid'],))
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

#修改種類
@app.route('/change_class/<int:cid>', methods=['PATCH'])
@token_required
def update_class(cid):
    try:
        data = request.get_json()
        new_class = data.get('class')
        new_money_limit = data.get('money_limit')

        if new_class is None or new_money_limit is None:
            return jsonify({'message': '請提供 class 和 money_limit', 'state': 'error'}), 400

        cur = mysql.connection.cursor()

        # 確認該 cid 是否存在
        cur.execute("SELECT * FROM class WHERE cid = %s", (cid,))
        existing = cur.fetchone()
        if not existing:
            return jsonify({'message': '找不到該筆資料', 'state': 'error'}), 404

        # 執行更新
        cur.execute(
            "UPDATE class SET class = %s, money_limit = %s WHERE cid = %s",
            (new_class, new_money_limit, cid)
        )
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': '更新成功', 'state': 'success'}), 200

    except Exception as e:
        print(f"[ERROR] 更新 class 發生錯誤：{e}")
        return jsonify({'message': '伺服器錯誤', 'state': 'error','error': str(e)}), 500

#刪除種類
@app.route('/delete_class/<int:cid>', methods=['DELETE'])
@token_required
def delete_class(cid):
    try:
        cur = mysql.connection.cursor()

        # 檢查該筆資料是否存在
        cur.execute("SELECT * FROM class WHERE cid = %s", (cid,))
        existing = cur.fetchone()

        if not existing:
            cur.close()
            return jsonify({'message': '找不到該筆資料', 'state': 'error'}), 404

        # 執行刪除
        cur.execute("DELETE FROM class WHERE cid = %s", (cid,))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': '刪除成功', 'state': 'success'}), 200

    except Exception as e:
        print(f"[ERROR] 刪除 class 發生錯誤：{e}")
        return jsonify({'message': '伺服器錯誤', 'state': 'error'}), 500

#新增種類
@app.route('/add_class', methods=['POST'])
@token_required
def add_class():
    try:
        data = request.get_json()
        new_class = data.get('class')
        money_limit = data.get('money_limit')

        if not new_class or money_limit is None:
            return jsonify({'message': '請提供 class 和 money_limit', 'state': 'error'}), 400

        cur = mysql.connection.cursor()

        # 檢查是否已有相同的 class 名稱
        cur.execute("SELECT * FROM class WHERE class = %s", (new_class,))
        existing = cur.fetchone()
        if existing:
            cur.close()
            return jsonify({'message': '類別名稱已存在，請使用不同名稱', 'state': 'error'}), 409

        # 新增資料
        cur.execute(
            "INSERT INTO class (class, money_limit) VALUES (%s, %s)",
            (new_class, money_limit)
        )
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': '新增成功', 'state': 'success'}), 201

    except Exception as e:
        print(f"[ERROR] 新增 class 發生錯誤：{e}")
        return jsonify({'message': '伺服器錯誤', 'state': 'error'}), 500

#會計科目
@app.route('/list_accounting', methods=['GET'])
@token_required
def list_accounting():
    try:
        class_name = request.args.get('class')

        if not class_name:
            return jsonify({'message': '請提供 class 參數', 'state': 'error'}), 400

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT account_class FROM accounting WHERE class = %s", (class_name,))
        results = cur.fetchall()
        cur.close()

        account_classes = [row['account_class'] for row in results]

        return jsonify({'message': '查詢成功','state': 'success','data': account_classes}), 200

    except Exception as e:
        print(f"[ERROR] 查詢 account_class 發生錯誤：{e}")
        return jsonify({'message': '伺服器錯誤', 'state': 'error'}), 500

#未核銷的發票
@app.route('/not_write_off', methods=['GET'])
@token_required
def not_write_off():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # 統計 status 為 0 的筆數
        cur.execute("SELECT COUNT(*) AS count_0 FROM Ticket WHERE status = 0")
        count_0 = cur.fetchone()['count_0']

        # 統計 status 為 1 的筆數
        cur.execute("SELECT COUNT(*) AS count_1 FROM Ticket WHERE status = 1")
        count_1 = cur.fetchone()['count_1']

        cur.close()

        total = count_0 + count_1

        return jsonify({
            'message': '統計成功',
            'state': 'success',
            'total': total
        }), 200

    except Exception as e:
        print(f"[ERROR] 統計 Ticket status 錯誤：{e}")
        return jsonify({'message': '伺服器錯誤', 'state': 'error'}), 500

#以核銷發票和金額
@app.route('/write_off', methods=['GET'])
@token_required
def write_off():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # 統計 Ticket 表中 status = 2 的筆數
        cur.execute("SELECT COUNT(*) AS status_2_count FROM Ticket WHERE status = 2")
        status_2_count = cur.fetchone()['status_2_count']

        # 加總 Ticket_detail 表中 money，條件是 Ticket 的 status = 2
        cur.execute("""
            SELECT SUM(td.money) AS total_money
            FROM Ticket_detail td
            JOIN Ticket t ON td.tid = t.tid
            WHERE t.status = 2
        """)
        result = cur.fetchone()
        total_money = result['total_money'] if result['total_money'] is not None else 0

        cur.close()

        return jsonify({'message': '統計成功','state': 'success','data': total_money}), 200

    except Exception as e:
        print(f"[ERROR] 統計 status=2 與金額加總錯誤：{e}")
        return jsonify({'message': '伺服器錯誤', 'state': 'error'}), 500


#修改顏色的值
@app.route('/change_color', methods=['PATCH'])
@token_required
def change_color():
    try:
        data = request.get_json()

        red_but = data.get('red_but')
        red_top = data.get('red_top')
        yellow_but = data.get('yellow_but')
        yellow_top = data.get('yellow_top')
        green_but = data.get('green_but')
        green_top = data.get('green_top')

        # 檢查欄位是否都存在
        required_fields = [red_but, red_top, yellow_but, yellow_top, green_but, green_top]
        if any(v is None for v in required_fields):
            return jsonify({'message': '請提供所有欄位資料', 'state': 'error'}), 400

        # 驗證條件
        if not (red_but <= red_top and yellow_but <= yellow_top and green_but <= green_top):
            return jsonify({'message': 'but 值不能大於 top', 'state': 'error'}), 400

        if not (red_top <= yellow_but and yellow_top <= green_but):
            return jsonify({'message': 'red 不可超過 yellow，yellow 不可超過 green', 'state': 'error'}), 400

        uid = g.user['uid']
        cur = mysql.connection.cursor()

        # 檢查是否已有設定資料
        cur.execute("SELECT * FROM other_setting WHERE uid = %s", (uid,))
        existing = cur.fetchone()

        if existing:
            cur.execute("""
                UPDATE other_setting SET 
                    red_but = %s, red_top = %s, 
                    yellow_but = %s, yellow_top = %s, 
                    green_but = %s, green_top = %s 
                WHERE uid = %s
            """, (red_but, red_top, yellow_but, yellow_top, green_but, green_top, uid))
        else:
            cur.execute("""
                INSERT INTO other_setting 
                    (uid, red_but, red_top, yellow_but, yellow_top, green_but, green_top)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (uid, red_but, red_top, yellow_but, yellow_top, green_but, green_top))

        mysql.connection.commit()
        cur.close()

        return jsonify({'message': '閾值更新成功', 'state': 'success'}), 200

    except Exception as e:
        print(f"[ERROR] 更新 other_setting 閾值失敗：{e}")
        return jsonify({'message': '伺服器錯誤', 'state': 'error'}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)