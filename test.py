from tools import Customer,Item,Lineitem,Orders,Sale,Admin


#print(Customer.alterusers(1,'wf',123,'小愤',123456,'上海'))
# print(Customer.query())
# print(Item.query(order=None))
#print(Item.basket_item_data(1))
# print(Customer.is_valid('王帆',123))
# print(Customer.is_repeated('王帆'))
# print(Customer.get_id_by_name("王帆") )
# print(Lineitem.get_item_data(2))
# print(Lineitem.get_item_id(9))
# print(Orders(1).get_max_order_list())
# Item.alteritem(1,'人间失物',23,'1.jpg',20,200,0.9)
# # print(Sale.get_discount_total('王帆'))
# print(Sale.getMinute('王帆'))
#print(Admin.saveDB('admin1',123,'管理员',123456,'安徽') )
print(Lineitem.get_singleorder_list(1) )