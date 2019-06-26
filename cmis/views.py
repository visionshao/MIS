from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import random
from datetime import datetime
from datetime import timedelta
from cmis.models import Sale
from cmis.models import SaleRecord
from cmis.models import Dish
from cmis.models import Food
from cmis.models import LeftFood
from cmis.models import OrderRecord
from cmis.models import Order
from cmis.models import Menu
from .models import *
import json
import datetime
import time
from sklearn.naive_bayes import MultinomialNB
import numpy as np



# Create your views here.
#首页
def index(request):
    context = {}
    return render(request, 'cmis/index.html', context)

#菜谱管理
def menuManagement(request):
    context = {}
    return render(request, 'cmis/menuManagement.html', context)


#预约管理
def appointManagement(request):
    context = {}
    return render(request, 'cmis/appointManagement.html', context)


#采购管理
def purchaseManagement(request):
    context = {}
    return render(request, 'cmis/purchaseManagement.html', context)


#订单管理
def ordersManagement(request):
    context = {}
    return render(request, 'cmis/ordersManagement.html', context)


#库存管理
def repertoryManagement(request):
    context = {}
    return render(request, 'cmis/repertoryManagement.html', context)


#销售管理
def saleManagement(request):
    context = {}
    return render(request, 'cmis/saleManagement.html', context)



#预测记录
def getPredictResult(request):
    getPredictResult = PredictFood()
    print("############")
    print(getPredictResult)
    return JsonResponse(getPredictResult, safe=False)



#所有库存记录
def getRepertoryResult(request):
    getRepertoryResult = allrepository()
    return JsonResponse(getRepertoryResult, safe=False)

#单个库存记录
def getSingleRepertoryResult(request):
    keyword = request.GET['keyword']
    print("$$$$$$$$$$$$$$$$$")
    print(keyword)
    SingleRepertoryResult = searchrepository(keyword)
    return JsonResponse(SingleRepertoryResult, safe=False)

#所有菜单记录
def getMenuResult(request):
    MenuResult = allmenu()
    return JsonResponse(MenuResult, safe=False)

#单个菜单记录
def getSingleMenuResult(request):
    keyword = request.GET['keyword']
    print("$$$$$$$$$$$$$$$$$")
    print(keyword)
    SingleMenuResult = searchmenu(keyword)
    return JsonResponse(SingleMenuResult, safe=False)


#所有订单记录
def getOrdersResult(request):
    ordersResult = finishedorders()
    return JsonResponse(ordersResult, safe=False)


#所有销售记录
def getSaleResult(request):
    time = request.GET['time']
    time=json.loads(time)
    print("#########################")
    print(time)
    getSaleResult = allsalerecord(time)
    return JsonResponse(getSaleResult, safe=False)

#单个销售记录
def getSingleSaleResult(request):
    keyword = request.GET['keyword']
    time = request.GET['time']
    print("$$$$$$$$$$$$$$$$$")
    print(keyword)
    SingleSaleResult = searchsalerecord(time, keyword)
    return JsonResponse(SingleSaleResult, safe=False)


# Create your views here.

#单个销售记录
def searchsalerecord(time, keyword=False):
    starttime = datetime(time['startYear'], time['startMonth'], time['startDay'])
    endtime = datetime(time['endYear'], time['endMonth'], time['endDay'])
    result = {}
    i = 1
    while starttime <= endtime:
        dishid = Dish.objects.get(name=keyword).values("id")
        saleids = Sale.objects.filter(time=starttime).values_list("id")
        summ = 0
        for saleid in saleids:
            q = SaleRecord.objects.filter(sale=saleid, dish=dishid).values("quantity")
            if q:
                summ += q['quantity']
        if summ != 0:
            result[i] = {"order": i, "date": starttime, "dishname":keyword, "quantity": summ}
            i += 1
        starttime += timedelta(days=1)
    return result


#所有销售记录
def allsalerecord(time):
    starttime = datetime(int(time['startYear']), int(time['startMonth']), int(time['startDay']))
    endtime = datetime(int(time['endYear']), int(time['endMonth']), int(time['endDay']))
    result = {}
    i = 1
    while starttime <= endtime:
        theDict = {}
        saleids = Sale.objects.filter(time=starttime).values_list("id")
        for saleid in saleids:
            print("###########")
            print(saleid)
            q = SaleRecord.objects.filter(sale=saleid[0]).values_list("dish", "quantity")
            for item in q:
                print(item)
                if item[0] not in theDict.keys():
                    theDict[item[0]] = item[1]
                else:
                    theDict[item[0]] += item[1]
        for key in theDict.keys():
            print("^^^^^^^^^^^^^^^")
            print(key)
            print(theDict[key])
            name = Dish.objects.filter(id=key).values("name")
            print(name)
            result[i] = ({"order": i, "date": starttime, "dishname": name[0]['name'], "quantity": theDict[key]})
            i = i+1
        starttime += timedelta(days=1)
    dic = {}
    for k in range(1,i):
        name = Dish.objects.filter(name=result[k]['dishname']).values("id")
        print(name)
        foods = Menu.objects.filter(dish=name[0]['id']).values_list("food", "quantity")
        for food in foods:
            print(food)
            foodname = Food.objects.filter(id=food[0]).values("name")
            print(foodname)
            total = food[1]*result[k]['quantity']
            if foodname[0]['name'] in dic.keys():
                dic[foodname[0]['name']] += total
            else:
                dic[foodname[0]['name']] = total
    return {"food": result, "statistic": dic}


#所有菜单
def allmenu():
    dishs = Dish.objects.all().values_list("id", "name")
    theDict = {}
    i = 1
    for dish in dishs:
        print("@@@@@@@@@@")
        print(dish)
        foods = Menu.objects.filter(dish=dish[0]).values_list("food", "quantity")
        strr = ""
        for food in foods:
            print("************")
            print(food)
            strr = strr + food[0] + " " + str(food[1]) + "g; "
        strr = strr[:-1]
        theDict[i] = {"order": i, "dishname": dish[1], "material": strr}
        i = i+1
    return theDict


#单个菜单
def searchmenu(keyword):
    dish = Dish.objects.filter(name=keyword).values("id", "name")
    foods = Menu.objects.filter(dish=dish[0]['id']).values_list("food", "quantity")
    print("$$$$$$$$$$$$")
    print(dish)
    print(foods)
    strr = ""
    for food in foods:
        print("&&&&&&&&&&")
        print(food)
        strr = strr + food[0] + " " + str(food[1]) + "g: "
    strr = strr[:-1]
    return {1: {"order": 1, "dishname": dish[0]['name'], "material": strr}}


#所有库存
def allrepository():
    foods = Food.objects.all().values_list("id", "name")
    theDict = dict()
    i = 1
    for food in foods:
        print("########")
        print(food)
        f = LeftFood.objects.filter(food=food[0]).values("leftNum")
        print(f)
        print(f[0]['leftNum'])
        theDict[i]={"order": i, "foodName": food[1], "leftQuantity": f[0]['leftNum']}
        i = i+1
    return theDict


#单个库存
def searchrepository(keyword):
    print("&&&&&&&&&&&&&&&&")
    print(keyword)
    food = Food.objects.filter(name=keyword).values("id")
    print(food)
    f = LeftFood.objects.filter(food=food[0]['id']).values("leftNum")
    print("#############")
    print(f)
    return {1: {"order": 1, "foodName": keyword, "leftQuantity": f[0]['leftNum']}}



#所有订单
def finishedorders():
    orders = OrderRecord.objects.all().values_list("order", "food", "quantity")
    theDict = {}
    i = 1
    for order in orders:
        print("###########")
        print(order)
        orderid = Order.objects.filter(id=order[0]).values("btime")
        print(orderid)
        foodid = Food.objects.filter(id=order[1]).values("name", "price")
        print(foodid)
        theDict[i] = {"biaohao": i, "orderid": order[0], "time": orderid[0]['btime'], "name": foodid[0]['name'], "price": foodid[0]['price'], "quantity": order[2]}
        i = i + 1
    return theDict

#------------------------预测函数-------------------------------

# 获取周
def getWeekDay(s):
    return s.strftime("%w")

# 判断时段
def getTimeField(s):
    if 0 <= s.hour < 11:
        return 0
    elif 11 <= s.hour < 14:
        return 1
    elif 14 <= s.hour < 24:
        return 2

def PredictFood():
    all_students = [item.id for item in list(Student.objects.all())]
    all_windows = [item.id for item in list(Window.objects.all())]
    all_dishes = [item.id for item in list(Dish.objects.all())]
    X_data = []
    for s in Sale.objects.all():
        srs = SaleRecord.objects.filter(sale=s.id)
        for sr in srs:
            x = [s.id, s.student.id, getWeekDay(s.time), getTimeField(s.time), s.window.id, sr.dish.id, sr.quantity]
            X_data.append(x)

    # 学生学号与数字转换
    sid = list(set(all_students))
    length = range(len(sid))
    sid2num_dict = dict(zip(sid, length))
    num2sid_dict = dict(zip(length, sid))
    # 窗口id与数字转换
    wid = list(set(all_windows))
    length = range(len(wid))
    wid2num_dict = dict(zip(wid, length))
    num2wid_dict = dict(zip(length, wid))
    # 菜品id与数字转换
    did = list(set([x[5] for x in X_data]))
    length = range(len(did))
    did2num_dict = dict(zip(did, length))
    num2did_dict = dict(zip(length, did))
    # 销售号，学生，周几，时段，窗口，菜品，菜量
    X_data = [[x[0], sid2num_dict[x[1]], eval(x[2]), x[3], wid2num_dict[x[4]], did2num_dict[x[5]], x[6]] for x in X_data]
    # 学生，周几，时段，窗口，菜品, 菜量
    X_data = np.array([[x[1], x[2], x[3], x[4], x[5], x[6]] for x in X_data])
    # 获取用于预测窗口的数据
    X1 = X_data[:, 0:3]
    y1 = X_data[:, 3:4]
    # 训练预测窗口的贝叶斯
    nb_model1 = MultinomialNB()
    nb_model1.fit(X1, y1)

    # 获取用于预测菜品的数据
    X2 = X_data[:, 0:4]
    y2 = X_data[:, 4:5]
    # 训练预测窗口的贝叶斯
    nb_model2 = MultinomialNB()
    nb_model2.fit(X2, y2)

    # 获取用于预测菜两的数据
    X3 = X_data[:, 0:5]
    y3 = X_data[:, 5:6]
    # 训练预测窗口的贝叶斯
    nb_model3 = MultinomialNB()
    nb_model3.fit(X3, y3)

    # 获取预约学生id
    AppointStudent = list(set([item.student for item in Appoint.objects.all()]))
    predict_students = list(set([item for item in all_students if item not in AppointStudent]))

    # 早上
    X_pre1 = [[sid2num_dict[item], eval(getWeekDay(datetime.datetime.today())) + 1, 0] for item in predict_students]
    # 中午
    X_pre2 = [[sid2num_dict[item], eval(getWeekDay(datetime.datetime.today())) + 1, 1] for item in predict_students]
    # 晚上
    X_pre3 = [[sid2num_dict[item], eval(getWeekDay(datetime.datetime.today())) + 1, 2] for item in predict_students]
    # 获取预测得到的窗口
    y_pre1 = nb_model1.predict(X_pre1)
    y_pre2 = nb_model1.predict(X_pre2)
    y_pre3 = nb_model1.predict(X_pre3)
    # 预测菜品
    X_pre1 = np.concatenate((np.array(X_pre1), np.array([y_pre1]).reshape(len(y_pre1), 1)), axis=1)
    X_pre2 = np.concatenate((np.array(X_pre2), np.array([y_pre2]).reshape(len(y_pre1), 1)), axis=1)
    X_pre3 = np.concatenate((np.array(X_pre3), np.array([y_pre3]).reshape(len(y_pre1), 1)), axis=1)

    y_pre1 = nb_model2.predict(X_pre1)
    y_pre2 = nb_model2.predict(X_pre2)
    y_pre3 = nb_model2.predict(X_pre3)
    # 预测菜量
    X_pre1 = np.concatenate((X_pre1, np.array([y_pre1]).reshape(len(y_pre1), 1)), axis=1)
    X_pre2 = np.concatenate((X_pre2, np.array([y_pre2]).reshape(len(y_pre1), 1)), axis=1)
    X_pre3 = np.concatenate((X_pre3, np.array([y_pre3]).reshape(len(y_pre1), 1)), axis=1)

    y_pre1 = nb_model3.predict(X_pre1)
    y_pre2 = nb_model3.predict(X_pre2)
    y_pre3 = nb_model3.predict(X_pre3)

    # 预测结果(学生，周几，时段，窗口，菜品，菜量）
    X_pre1 = np.concatenate((X_pre1, np.array([y_pre1]).reshape(len(y_pre1), 1)), axis=1)
    X_pre2 = np.concatenate((X_pre2, np.array([y_pre2]).reshape(len(y_pre1), 1)), axis=1)
    X_pre3 = np.concatenate((X_pre3, np.array([y_pre3]).reshape(len(y_pre1), 1)), axis=1)

    X_pre = np.concatenate((X_pre1, X_pre2, X_pre3), axis=0)

    result = dict() # 单位为克
    for item in X_pre:
        dish_id = num2did_dict[item[-2]]

        Menu_set = Menu.objects.filter(dish=dish_id)

        for it in Menu_set:
            name = it.food.name
            if name  not in result:
                result[name] = it.quantity * item[-1]
            else:
                result[name] += it.quantity * item[-1]

    # for k, v in result.items():
    #     p = Prediction()
    #     p.food = Food.objects.get(name=k)
    #     p.quentity = v / 1000
    #     p.save()

    return result
