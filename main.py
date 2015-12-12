#!/usr/bin/env python
# coding=utf-8
'''
Created on 2015年12月12日

@author: wanghan
'''
from selenium import webdriver
from time import sleep

ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
confirm_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

chromedriver_path = "/usr/local/bin/chromedriver"

button_chaxun_id = "query_ticket"  # #查询按钮ID
button_login_id = "loginSub"
text_shifazhan_id = "fromStationText"
text_zhongdianzhan_id = "toStationText"
text_riqi_id = "train_date"
text_username_id = "username"
text_password_id = "password"
text_chengke_id = "normal_passenger_id"

value_username = "******"
value_password = "******"
value_fromstation = '%u5317%u4EAC%2CBJP'
value_tostation = "%u90D1%u5DDE%2CZZF"
value_date = "2015-12-13"

# value_checi = ["G89", "G87"]  # #按照车次的优先级放入 如果是空的话 就表示当天任意一个班次
value_checi = [] 
value_chengke = ["王晗"]

value_shuaxinpinlv = 2
class HuochePiao:
    def __init__(self):
        global brower
        brower = webdriver.Chrome(chromedriver_path)
        
    # #开始刷票
    def start(self):
        print "开始刷票..."
        self.login()
        self.list()
        self.order()    
        
    # #登录
    def login(self):
        brower.get(login_url)
        sleep(2)
        brower.find_element_by_id(text_username_id).send_keys(value_username)
        brower.find_element_by_id(text_password_id).send_keys(value_password)
        brower.execute_script("alert('请自行选择验证码')")
        while True:
            sleep(2)
            if brower.current_url == initmy_url:
                print "登录成功,进入查询页面"
                break
    # #进入车票列表页
    def list(self):
        brower.get(ticket_url)
        brower.add_cookie({"name":"_jc_save_fromStation", "value":value_fromstation})
        brower.add_cookie({"name":"_jc_save_toStation", "value":value_tostation})
        brower.add_cookie({"name":"_jc_save_fromDate", "value":value_date})
        brower.refresh()
        cheCi = self.chaxun()
        if cheCi != None:
            cheCi.click()
    
    # #车票刷新        
    def chaxun(self):
        chaxunBtn = brower.find_element_by_id(button_chaxun_id)
        yudingBtns = []
        checi = None
        count = 1
        while True:
            chaxunBtn.click()
#             JsUtil.showShuxin(brower, count)
            count = count + 1
            sleep(value_shuaxinpinlv)
            yudingBtns = brower.find_elements_by_class_name("btn72")
            if(len(yudingBtns) > 0):
                # #车次优先
                if(len(value_checi) > 0):
                    tmp = {}
                    for b in yudingBtns:
                        try:
                            ccName = b.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_class_name("number").text.encode('utf-8')
                            if ccName in value_checi:
                                tmp[ccName] = b
                        except:
                            pass
                    for cc in value_checi:
                        if cc in tmp:
                            checi = tmp[cc]
                            break
                    if checi != None:
                        break
                # #没有指定车次
                else:
                    checi = yudingBtns[0]
                    break
        return checi
    
    # #进入订单页
    def order(self):
        while brower.current_url != confirm_url:
            sleep(2)
        chengkeParent = brower.find_element_by_id(text_chengke_id).find_elements_by_tag_name("li")
        for p in chengkeParent:
            if p.find_element_by_tag_name("label").text.encode('utf-8') in value_chengke:
                p.find_element_by_tag_name("input").click()
        brower.execute_script("alert('请选择验证码并提交订单')")
if __name__ == '__main__':
    cp = HuochePiao()
    cp.start()
