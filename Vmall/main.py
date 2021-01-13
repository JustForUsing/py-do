import time

from selenium import webdriver


# 根据文本获取dom对象
def get_obj(aim, target):
    order_pay_obj = object()
    try:
        if aim == 'text':
            order_pay_obj = browser.find_element_by_link_text(target)
        elif aim == 'id':
            order_pay_obj = browser.find_element_by_id(target)
        else:
            order_pay_obj = browser.find_element_by_css_selector('#' + target)

        if 'disabled' in order_pay_obj.get_attribute('class'):
            print(target+'按钮禁用中')
            raise Exception('禁用中')
    except:
        if target == '提前登录':
            return 'false'

        print('get ' + target + ' dom failed')
        time.sleep(0.1)
        get_obj(aim, target)
    return order_pay_obj


# 防止页面刷新，点击异常捕获
def obj_click(obj_aim, obj_target):
    try:
        get_obj(obj_aim, obj_target).click()
    except:
        print('click' + obj_target + ' failed')
        time.sleep(0.1)
        obj_click(obj_aim, obj_target)


# 打开Chrome浏览器
browser = webdriver.Chrome()
# browser.get("file:///C:/Users/Sovell Pc/Desktop/next.html")
browser.get("https://www.vmall.com/product/10086998928105.html")
print('Get page finished')

# 判断是否需要登陆
login_obj = get_obj('text', '请登录')
if type(login_obj) != str:
    print('Login_time')
    login_obj.click()
    time.sleep(60)
    print('Login time finished')

print('选择型号')
obj_click('text', '秘银色')

print('点击支付定金')
obj_click('text', '支付订金')

print('点击提交订单')
obj_click('text', '提交订单')
