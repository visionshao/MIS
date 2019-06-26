from django.db import models


# Create your models here.
class Student(models.Model):
    # 学生类
    id = models.CharField(max_length=10, primary_key=True)


class Dish(models.Model):
    # 菜品
    id = models.CharField(max_length=10, primary_key=True)
    # 菜品id
    name = models.CharField(max_length=30)
    # 菜品名


class Window(models.Model):
    # 窗口类
    id = models.CharField(max_length=11, primary_key=True)
    # 窗口编号
    canteen = models.ForeignKey("Canteen", to_field="id", on_delete=models.CASCADE)
    # 所属食堂id
    name = models.CharField(max_length=18)
    # 窗口名


class WindowDish(models.Model):
    # 窗口对应的菜
    window = models.ForeignKey("Window", to_field="id", on_delete=models.CASCADE)
    # 窗口id
    dish = models.ForeignKey("Dish", to_field="id", on_delete=models.CASCADE)
    # 菜品id


class Order(models.Model):
    # 订单记录
    id = models.CharField(max_length=10, primary_key=True)
    # id
    btime = models.DateTimeField()
    # 订单生成时间


class OrderRecord(models.Model):
    # d订单明细
    order = models.ForeignKey("Order", to_field="id", on_delete=models.CASCADE)
    # 订单id
    food = models.ForeignKey("Food", to_field="id", on_delete=models.CASCADE)
    # 食材id
    quantity = models.FloatField(max_length=12)
    # 数量


class LeftFood(models.Model):
    # 剩余库存
    # 食材
    food = models.ForeignKey("Food", to_field="id", on_delete=models.CASCADE)
    # 剩余量
    leftNum = models.FloatField(max_length=10)


class Food(models.Model):
    # 食材表
    # id
    objects = models.Manager()
    id = models.CharField(max_length=11, primary_key=True)
    # 名字
    name = models.CharField(max_length=50)
    # 价格
    price = models.FloatField(max_length=12)


class Sale(models.Model):
    # 销售单
    id = models.CharField(max_length=10, primary_key=True)
    # 销售记录id
    time = models.DateTimeField()
    # 时间
    window = models.ForeignKey("Window", to_field="id", on_delete=models.CASCADE)
    # 销售窗口
    student = models.ForeignKey("Student", to_field="id", on_delete=models.CASCADE)


class SaleRecord(models.Model):
    # 销售类
    sale = models.ForeignKey("Sale", to_field="id", on_delete=models.CASCADE)
    # 菜品编号
    dish = models.ForeignKey("Dish", to_field="id", on_delete=models.CASCADE)
    # 分数
    quantity = models.FloatField(max_length=2)


class Menu(models.Model):
    # 菜谱类
    dish = models.ForeignKey("Dish", to_field="id", on_delete=models.CASCADE)
    # 菜品名
    food = models.ForeignKey("Food", to_field="id", on_delete=models.CASCADE)
    # 食材名
    quantity = models.FloatField(max_length=10)
    # 所需食材量


class Canteen(models.Model):
    # 食堂
    id = models.CharField(max_length=10, primary_key=True)
    # 食堂id
    name = models.CharField(max_length=12)
    # 食堂名


class Appoint(models.Model):
    # 预约
    id = models.CharField(max_length=10, primary_key=True)
    # 预约单id
    student = models.ForeignKey("Student", to_field="id", on_delete=models.CASCADE)
    # 学号
    time = models.DateTimeField()
    # 时间
    window = models.ForeignKey("Window", to_field="id", on_delete=models.CASCADE)
    # 窗口


class AppointmentRecord(models.Model):
    # 预约明细
    appoint = models.ForeignKey("Appoint", to_field="id", on_delete=models.CASCADE)
    # 预约id
    dish = models.ForeignKey("Dish", to_field="id", on_delete=models.CASCADE)
    # 预约菜品id
    quantity = models.FloatField(max_length=10)
    # 数量


class Prediction(models.Model):
    # 食材ID
    food = models.ForeignKey("Food", to_field="id", on_delete=models.CASCADE)
    # 数量
    quentity = models.FloatField(max_length=12)


