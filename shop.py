from flask import Flask,render_template,request,url_for,redirect,session,flash
from tools import Customer,Item,Sale,Orders,Lineitem,Seller,Admin

app = Flask(__name__)
app.secret_key='666'

@app.route('/')
def index():
    booklist = Item.query()
    session['booklist'] = booklist
    return render_template('index.html')

@app.route('/custommer_index.page')
def customer_index():
    booklist = Item.query()
    session['booklist']=booklist
    session['customer_data'] = Customer.query()
    return render_template('customerindex.html')

@app.route('/seller_index.page')
def seller_index():
    session['item_data']=Item.query(order=None)
    session['allorder_data']=Lineitem.get_allorder_list()
    return render_template('sellerindex.html')

@app.route('/admin_index.page')
def admin_index():
    session['customer_data'] = Customer.query()
    session['seller_data']= Seller.query()
    return render_template('adminindex.html')

@app.route('/index_to_login')
def index_to_login():
    return render_template('login.html')

@app.route('/to_register.page')
def register_page():
    return render_template('register.html')

@app.route('/single_item')
def detail():
    return render_template('single.html')

@app.route('/login_to_index',methods=['POST'])
def login():
    form = request.form
    username = form.get('name')
    password = form.get('pwd')
    role=form.get('select')
    if Customer.is_valid(username,password):
        session['name']=username
        session['userId']=Customer.get_id_by_name(username)
        if role == u'顾客':
            session['minute'] = Sale.getMinute(username)
            session['id']=Customer.get_id_by_name(username)
            session['basket_data'] = Item.basket_item_data(Customer.get_id_by_name(username))
            session['order_data']=Lineitem.get_singleorder_list(Customer.get_id_by_name(username))
            session['total'] = Sale.get_total(username)
            session['discount_total']=Sale.get_discount_total(username)
            session['overthreshold_total']=Sale.get_overthreshold_total(username)
            return redirect(url_for('customer_index'))
        else:
            flash('账号或密码错误')
            return render_template('login.html')
    elif Seller.is_valid(username,password):
        session['name']=username
        if role==u'卖家':
            return redirect(url_for('seller_index'))
        else:
            flash('账号或密码错误')
            return render_template('payment.html')
    elif Admin.is_valid(username,password):
        session['name'] = username
        if role == u'管理员':
            return redirect(url_for('admin_index'))
        else:
            flash('账号或密码错误')
            return render_template('orders.html')
    else:
        flash('该用户不存在，请重新输入')
        return render_template('login.html')

@app.route('/register',methods=['POST'])
def register():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    nickname=form.get('nickname')
    telephone=form.get('phone')
    address=form.get('address')
    role = form.get('select')

    if role==u"买家":
        if not username:
            flash("请输入用户名")
            return render_template("register.html")
        if not password:
            flash("请输入密码")
            return render_template("register.html")
        if not Customer.is_repeated(username):
            session['name']=username
            Customer.saveDB(username, password, nickname, telephone, address)
            session['customer_data'] = Customer.query()
            return redirect(url_for('customer_index'))
        else:
            flash('用户名重复')
            return render_template('register.html')
    elif role==u"卖家":
        if not username:
            flash("请输入用户名")
            return render_template("register.html")
        if not password:
            flash("请输入密码")
            return render_template("register.html")
        if not Seller.is_repeated(username):
            session['name'] = username
            Seller.saveDB(username, password, nickname, telephone, address)
            session['seller_data'] = Seller.query()
            return redirect(url_for('seller_index'))
        else:
            flash('用户名重复')
            return render_template('register.html')
    elif role==u"管理员":
        if not username:
            flash("请输入用户名")
            return render_template("register.html")
        if not password:
            flash("请输入密码")
            return render_template("register.html")
        if not Admin.is_repeated(username):
            session['name'] = username
            Admin.saveDB(username, password,nickname,telephone,address)
            return redirect(url_for('admin_index'))
        else:
            flash('用户名重复')
            return render_template('register.html')
    else:
        flash("请重新选择注册角色")
        return render_template('register.html')

@app.route('/customer_register',methods=['POST'])
def custommer_register():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    nickname=form.get('nickname')
    telephone=form.get('phone')
    address=form.get('address')

    if not username:
        flash("请输入用户名")
        return render_template("register.html")
    if not password :
        flash("请输入密码")
        return render_template("register.html")
    if not Customer.is_repeated(username):
        Customer.saveDB(username,password,nickname,telephone,address)
        session['customer_data'] = Customer.query()
        return redirect(url_for('admin_index'))
    else:
        flash('用户名重复')
        return render_template('adminindex.html')

@app.route('/alter_customer/<user_id>', methods=['POST'])
def alteruser(user_id):
    form=request.form
    username = form.get('username')
    password = form.get('password')
    nname = form.get('nickname')
    telephone = form.get('phone')
    address = form.get('address')
    print(user_id)
    if not Customer.is_repeated(username):
        Customer.alterusers(user_id,username,password,nname,telephone,address)
        session['name']=username
        session['basket_data'] = Item.basket_item_data(Customer.get_id_by_name(username))
        session['order_data'] = Lineitem.get_singleorder_list(Customer.get_id_by_name(username))
        session['customer_data'] = Customer.query()
        return redirect(url_for('customer_index'))
    else:
        flash('用户名重复')
        return redirect(url_for('customer_index'))

@app.route('/seller_register', methods=['POST'])
def seller_register():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    nickname = form.get('nickname')
    telephone = form.get('phone')
    address = form.get('address')

    if not username:
        flash("请输入用户名")
        return render_template("register.html")
    if not password:
        flash("请输入密码")
        return render_template("register.html")
    if not Seller.is_repeated(username):
        Seller.saveDB(username, password, nickname, telephone, address)
        session['seller_data'] = Seller.query()
        return redirect(url_for('admin_index'))
    else:
        flash('用户名重复')
        return render_template('adminindex.html')

@app.route('/delete_customer/<user_id>')
def del_customer(user_id):
    Customer.delete_customer(user_id)
    session['customer_data'] = Customer.query()
    return redirect(url_for('admin_index'))

@app.route('/delete_seller/<user_id>')
def del_seller(user_id):
    Seller.delete_seller(user_id)
    session['seller_data'] = Seller.query()
    return redirect(url_for('admin_index'))

@app.route('/alter_seller/<user_id>',methods=['POST'])
def seller_alteruser(user_id):
    form=request.form
    username = form.get('username')
    password = form.get('password')
    nname = form.get('nickname')
    telephone = form.get('phone')
    address = form.get('address')

    if not Seller.is_repeated(username):
        Seller.alterusers(user_id,username,password,nname,telephone,address)
        session['seller_data'] = Seller.query()
        return redirect(url_for('admin_index'))
    else:
        flash('用户名重复')
        return render_template('adminindex.html')


@app.route('/logout.page')
def logout():
    return redirect(url_for('index'))

@app.route('/basket.page')
def basket():
    return render_template('basket.html')

@app.route('/add_to_basket',methods=['POST'])
def add_to_basket():
    form = request.form
    username=form.get('username')
    item_id=form.get('item_id')
    if not username:
        return redirect(url_for('index_to_login'))
    sale = Sale(username)
    sale.add_item(item_id)
    session['basket_data'] = Item.basket_item_data(Customer.get_id_by_name(username))
    session['order_data'] = Lineitem.get_singleorder_list(Customer.get_id_by_name(username))
    session['total']=Sale.get_total(username)
    session['discount_total'] = Sale.get_discount_total(username)
    session['overthreshold_total'] = Sale.get_overthreshold_total(username)
    return redirect(url_for('customer_index'))

@app.route('/delete_item_from_basket/order_id=<order_id>,lineitem_id=<lineitem_id>,username=<username>')
def delete_item(order_id,lineitem_id,username):
    Orders.delete_from_basket(order_id,lineitem_id)
    session['basket_data'] = Item.basket_item_data(Customer.get_id_by_name(username))
    session['order_data'] = Lineitem.get_singleorder_list(Customer.get_id_by_name(username))
    session['total'] = Sale.get_total(username)
    session['discount_total'] = Sale.get_discount_total(username)
    session['overthreshold_total'] = Sale.get_overthreshold_total(username)
    return redirect(url_for('basket'))

@app.route('/delete_item_form_DB/<item_id>')
def delete_item1(item_id):
    Item.delete_item_from_DB(item_id)
    session['item_data'] = Item.query(order=None)
    return redirect(url_for('seller_index'))

@app.route('/checkout/<username>')
def checkout(username):
    sale = Sale(username)
    sale.checkout()
    session['basket_data'] = Item.basket_item_data(Customer.get_id_by_name(username))
    session['order_data'] = Lineitem.get_singleorder_list(Customer.get_id_by_name(username))
    session['total']=0
    session['discount_total'] = Sale.get_discount_total(username)
    session['overthreshold_total'] = Sale.get_overthreshold_total(username)
    return redirect(url_for('payment'))

@app.route('/payment.page')
def payment():
    return render_template('payment.html')

@app.route('/order.page/<username>')
def order(username):
    session['order_data'] = Lineitem.get_singleorder_list(Customer.get_id_by_name(username))
    return render_template('orders.html')

@app.route('/add_item',methods=['post'])
def additem():
    form = request.form
    item_name = form.get('itemname')
    item_price = form.get('itemprice')
    item_image = form.get('itemimage')
    discount=form.get('discount')
    threshold=form.get('threshold')
    percentage=form.get('percentage')

    Item.saveDB(item_name,item_price,item_image,discount,threshold,percentage)
    session['item_data']=Item.query(order=None)
    return redirect(url_for('seller_index'))

@app.route('/alter_item/<item_id>',methods=['post'])
def alteritem(item_id):
    form=request.form
    itemname=form.get('itemname')
    itemprice=form.get('itemprice')
    itemimage=form.get('itemimage')
    discount = form.get('discount')
    threshold = form.get('threshold')
    percentage = form.get('percentage')
    Item.alteritem(item_id,itemname,itemprice,itemimage,discount,threshold,percentage)
    session['item_data']=Item.query(order=None)
    return redirect(url_for('seller_index'))

if __name__ == '__main__':
    app.run()

