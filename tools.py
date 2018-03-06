import sqlite3,datetime

def sql_statement(sql):
    conn = sqlite3.connect("shopDB.db")
    cursor = conn.cursor()
    rows = cursor.execute(sql)
    list = []
    for row in rows:
        list.append(row)
    conn.commit()
    cursor.close()
    conn.close()
    return list
def sql_statement1(sql):
    conn = sqlite3.connect("shopDB.db")
    cursor = conn.cursor()
    rows = cursor.execute(sql)
    for row in rows:
        result = row[0]
        conn.commit()
        cursor.close()
        conn.close()
        return result
    return None
def sql_statement2(sql):
    conn = sqlite3.connect("shopDB.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

#添加买家、买家
def sql_statement3(sql,username, password, nickname, telephone, address):
    conn = sqlite3.connect("shopDB.db")
    cursor = conn.cursor()
    cursor.execute(sql, (username, password, nickname, telephone, address))
    conn.commit()
    cursor.close()
    conn.close()
#判断登陆的用户是否在数据库中
def valid(username,password,list):
    for i in list:
        if username == i[1] and password == i[2]:
            return True
    return False
#判断注册的用户是否与数据库中用户重名
def repeated(name,list):
    for i in list:
        if name == i[1]:
            return True
    return False


#Customer
class Customer(object):
    def __init__(self,c_id,c_name,c_password,c_nickname,c_phone,c_address):
        self.c_id=c_id
        self.c_name=c_name
        self.c_password=c_password
        self.c_nickname=c_nickname
        self.c_phone=c_phone
        self.c_address=c_address

    @staticmethod
    def query():
        sql = "select * from customer"
        list=sql_statement(sql)
        return list

    @staticmethod
    def is_valid(username, password):
        list = Customer.query()
        result = valid(username, password, list)
        return result

    @staticmethod
    def is_repeated(name):
        list=Customer.query()
        result=repeated(name,list)
        return result

    @staticmethod
    def get_id_by_name(name):
        sql = "select cId from customer where cName='" + name + "'"
        c_id=sql_statement1(sql)
        return c_id

    @staticmethod
    def saveDB(username,password,nickname,telephone,address):
        sql = "insert into customer VALUES (NULL,?,?,?,?,?)"
        sql_statement3(sql,username, password, nickname, telephone, address)

    @staticmethod
    def delete_customer(user_id):
        sql = "delete from customer where cId=" + str(user_id)
        sql_statement2(sql)

    @staticmethod
    def alterusers(userId,username,password,nname,telephone,address):
        sql = "update customer set cName='"+\
               username + "',cPassword="\
              + str(password) + " ,cNname='" \
              + nname + "',cPhone="\
              + str(telephone) + ",cAddress='"\
              + address + "' where cId = "+str(userId)
        sql_statement2(sql)

# Seller
class Seller():
    def __init__(self, s_id, s_name, s_password, s_nickname, s_phone, s_address):
        self.s_id = s_id
        self.s_name = s_name
        self.s_password = s_password
        self.s_nickname = s_nickname
        self.s_phone = s_phone
        self.s_address = s_address
# 查询所有卖家
    @staticmethod
    def query():
        sql = "select * from seller"
        list = sql_statement(sql)
        return list
# 卖家表是否含有此卖家
    @staticmethod
    def is_valid(username, password):
        list = Seller.query()
        result = valid(username, password, list)
        return result
# 查看注册的用户名是否有和数据库表中相同的
    @staticmethod
    def is_repeated(name):
        list = Seller.query()
        result = repeated(name, list)
        return result
# 添加新的卖家
    @staticmethod
    def saveDB(username, password, nickname, telephone, address):
        sql = "insert into seller VALUES (NULL,?,?,?,?,?)"
        sql_statement3(sql, username, password, nickname, telephone, address)
# 删除卖家
    @staticmethod
    def delete_seller(user_id):
        sql = "delete from seller where sId=" + str(user_id)
        sql_statement2(sql)
# 修改卖家信息
    @staticmethod
    def alterusers(userId, username, password, nname, telephone, address):
        sql = "update seller set sName='" + \
                username + "', sPassword=" \
                + str(password) + " , sNname='" \
                + nname + "' , sPhone=" \
                + str(telephone) + " , sAddress='" \
                + address + "' where sId = " + str(userId)
        sql_statement2(sql)

# Admin
class Admin():
    def __init__(self, a_id, a_name, a_password):
        self.a_id = a_id
        self.a_name = a_name
        self.a_password = a_password
            # 查找admin表中所有管理员

    @staticmethod
    def query():
        sql = "select * from admin"
        conn = sqlite3.connect("shopDB.db")
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        list = []
        for row in rows:
            list.append(row)
        conn.commit()
        cursor.close()
        conn.close()
        return list
# 卖家表是否含有此管理员
    @staticmethod
    def is_valid(username, password):
        list = Admin.query()
        result = valid(username, password, list)
        return result
# 查看注册的用户名是否有和数据库表中相同的
    @staticmethod
    def is_repeated(name):
        list = Admin.query()
        result = repeated(name, list)
        return result
# 添加管理员
    @staticmethod
    def saveDB(username, password,nickname,telephone,address):
        sql = "insert into admin VALUES (NULL,?,?,?,?,?)"
        sql_statement3(sql, username, password, nickname, telephone, address)

#Item
class Item(object):
    def __init__(self,item_id,item_name=None,item_price=None,item_image=None,discount=None,threshold=None,percentage=None):
        self.item_id=item_id
        self.item_name=item_name
        self.item_price=item_price
        self.item_image=item_image
        self.discount=discount
        self.threshold=threshold
        self.percentage=percentage

    @staticmethod
    def query(order=None):
        if order:
            sql = "select * from item desc order by itemId " + order
        else:
            sql = "select * from item desc order by itemId"
        list = sql_statement(sql)
        return list

    def get_item_name(self):
        sql="select itemName from item where itemId="+str(self.item_id)
        c_id = sql_statement1(sql)
        return c_id

    def get_item_price(self):
        sql = "select itemPrice from item where itemId=" + str(self.item_id)
        conn = sqlite3.connect("shopDB.db")
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        for row in rows:
            item_price = row[0]
            conn.commit()
            cursor.close()
            conn.close()
            return item_price

    def get_item_data_by_item_id(item_id):
            sql = "select * from item where itemId=" + str(item_id)
            conn = sqlite3.connect("shopDB.db")
            cursor = conn.cursor()
            rows = cursor.execute(sql)
            for row in rows:
                item_data = row
                conn.commit()
                cursor.close()
                conn.close()
                return item_data

    @staticmethod
    def basket_item_data(user_id):
            sql = " select orders.orderId,lineitem.lineitemId,lineitem.quantity,item.*  from lineitem,orders,item where lineitem.lineitemId=orders.lineitemId and lineitem.itemId=item.itemId and orders.status=0 and orders.cId=" + str(user_id)
            # order_id,lineitem_id,quantity,item_id,type,name,price,description,image
            list = sql_statement(sql)
            return list

    @staticmethod
    def saveDB(itemname, itemprice, itemimage,discount,threshold,percentage):
        sql = "insert into item VALUES (NULL,?,?,?,?,?,?)"
        conn = sqlite3.connect("shopDB.db")
        cursor = conn.cursor()
        cursor.execute(sql, (itemname, itemprice, itemimage,discount,threshold,percentage))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def alteritem(item_id,item_name,item_price,item_image,discount,threshold,percentage):
        sql = "update item set itemName='"+\
               item_name + "', itemPrice="\
              + str(item_price) + " , itemImage='" \
              + item_image + "' , discount='" \
              +str(discount)+"' , threshold='" \
              +str(threshold)+"' , percentage='" \
              +str(percentage)+"' where itemId = "+str(item_id)
        sql_statement2(sql)

    @staticmethod
    def delete_item_from_DB(item_id):
        sql = "delete from item where itemId=" + str(item_id)
        sql_statement2(sql)

#Lineitem
class Lineitem:
    def __init__(self,lineitem_id,item_id,quantity):
        self.lineitem_id = lineitem_id
        self.item_id = item_id
        self.quantity = quantity
        self.p=Item(item_id=item_id)

    def get_item_name(self):
        return self.p.get_item_name()

    def get_sum(self):
        return self.p.get_item_price()*self.quantity

    @staticmethod
    def get_item_data(lineitem_id):
        sql = "select itemId from lineitem where lineitemId=" + str(lineitem_id)
        item_id = sql_statement1(sql)
        return Item.get_item_data_by_item_id(item_id)

    @staticmethod
    def get_singleorder_list(user_id):
        sql = "select orders.orderList,lineitem.lineitemId,lineitem.quantity,item.*  from lineitem,orders,item where lineitem.lineitemId=orders.lineitemId and lineitem.itemId=item.itemId and orders.status=1 and orders.cId=" + str(user_id)
        # orderList,cid,lineitem_id,quantity,item_id,type,name,price,description,image
        list = sql_statement(sql)
        return list

    @staticmethod
    def get_allorder_list():
        sql = "select orders.orderList,orders.cId,lineitem.lineitemId,lineitem.quantity,item.*  from lineitem,orders,item where lineitem.lineitemId=orders.lineitemId and lineitem.itemId=item.itemId and orders.status=1 "
        # orderList,lineitem_id,quantity,item_id,type,name,price,description,image
        list = sql_statement(sql)
        return list

    @staticmethod
    def is_exist(item_id):
        sql = "select lineitemId from lineitem where itemId=" + str(item_id)
        conn = sqlite3.connect("shopDB.db")
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        lists =[]
        for row in rows:
            lists.append(row[0])
        conn.commit()
        cursor.close()
        conn.close()
        return lists

    @staticmethod
    def get_item_id(lineitem_id):
        sql = "select itemId from lineitem where lineitemId=" + str(lineitem_id)
        item_id=sql_statement1(sql)
        return item_id

    @staticmethod
    def add_one(lineitem_id):
        sql = "update lineitem set quantity = quantity+1 where lineitemId="+str(lineitem_id)
        sql_statement2(sql)

#Orders
class Orders(object):
    def __init__(self,user_id):
        self.user_id=user_id
        sql = "select orderList,lineitemId from orders where cId="+str(user_id)+"  and status =0"
        conn = sqlite3.connect("shopDB.db")
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        basket={}
        for row in rows:
            if row[0] in basket.keys():
                basket[row[0]].append(row[1])
            else:
                basket[row[0]]=[]
                basket[row[0]].append(row[1])
        conn.commit()
        cursor.close()
        conn.close()
        self.basket=basket

    def get_basket(self):
        return self.basket

    def get_max_order_list(self):
        sql = "select max(orderList) from orders where cId=" + str(self.user_id)
        max = sql_statement1(sql)
        return max

    def checkout(self):
        item_data =Item.basket_item_data(self.user_id)
        max = self.get_max_order_list()
        sql = "update orders set orderList = "+str(max+1)+" where cId="+str(self.user_id)+" and status=0"
        sql_statement2(sql)

        sql = "update orders set status = 1 where cId="+str(self.user_id)+" and status=0"
        sql_statement2(sql)

    def add_item(self,user_id,item_id):
        sql = "select lineitemId  from lineitem join (select lineitemId as it,status from orders) t on (lineitem.lineitemId=t.it and t.status=0 and lineitem.itemId="+str(item_id)+")"
        conn = sqlite3.connect("shopDB.db")
        cursor = conn.cursor()
        rows = cursor.execute(sql)
        p = 0
        for row in rows:
            if row[0]:
                Lineitem.add_one(row[0])
                p = 1
                break
        conn.commit()
        cursor.close()
        conn.close()

        if p==0:
            sql = "insert into lineitem VALUES (NULL,"+str(item_id)+",1)"
            sql_statement2(sql)

            sql = "select lineitemId  from lineitem  where itemId="+str(item_id)+" order by lineitemId desc  "
            conn = sqlite3.connect("shopDB.db")
            cursor = conn.cursor()
            rows = cursor.execute(sql)
            t=None
            for row in rows:
                t=row[0]
                conn.commit()
                cursor.close()
                conn.close()
                break;

            sql = "insert into orders VALUES (NULL,0,?,?,0)"
            conn = sqlite3.connect("shopDB.db")
            cursor = conn.cursor()
            cursor.execute(sql, (t, user_id))
            conn.commit()
            cursor.close()
            conn.close()

    @staticmethod
    def delete_from_basket(order_id,lineitem_id):
        sql = "delete from orders where orderId=" + str(order_id)
        sql_statement2(sql)

        sql = "delete from lineitem where lineitemId=" + str(lineitem_id)
        sql_statement2(sql)

#Sale
class Sale(object):
    def __init__(self,username):
        self.user_id=Customer.get_id_by_name(username)

    def checkout(self):
        o=Orders(self.user_id)
        o.checkout()

    def add_item(self,item_id):
        o = Orders(self.user_id)
        o.add_item(self.user_id, item_id)

    @staticmethod
    def add_to_basket(user_id, item_id):
        # return the item_id
        order = Orders(user_id)
        basket = order.get_basket()
        for b in basket.keys():
            lit = basket[b]
            for i in lit:
                if Lineitem.get_item_id(i) == item_id:
                    return 1
        Orders.add_item(user_id, item_id)
        return 1

    @staticmethod
    def get_total(user_name):
        lists = Item.basket_item_data(Customer.get_id_by_name(user_name))
        sum = 0
        for list in lists:
            sum = sum + list[2] * list[5]
        return sum

    @staticmethod
    def get_discount_total(user_name):
        result=Sale.get_total(user_name)
        sql='select percentage from item'
        percentage=sql_statement1(sql)
        sum=percentage*result
        return sum

    @staticmethod
    def get_overthreshold_total(user_name):
        result = Sale.get_total(user_name)
        sql = 'select threshold from item'
        threshold = sql_statement1(sql)
        sql = 'select discount from item'
        discount = sql_statement1(sql)
        if result<threshold:
            return result
        else:
            return result-discount

    def getMinute(username):
        cur = datetime.datetime.now()
        minute = cur.minute
        return minute






