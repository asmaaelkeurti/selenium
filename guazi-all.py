from selenium import webdriver
import pandas as pd
import time
import os.path
from datetime import date

l_list = [['https://www.guazi.com/www/buy/c-1f3/#bread','EV'],              #电动
           ['https://www.guazi.com/www/buy/c-1f1/#bread','gas'],            #汽油
         ['https://www.guazi.com/www/buy/c-1f4/#bread','hybrid']]           #油电混动



#link_data
def get_car_link(driver):
    l_list = ['https://www.guazi.com/www/buy/c-1f1/#bread',         #汽油
              'https://www.guazi.com/www/buy/c-1f3/#bread',         #电动
              'https://www.guazi.com/www/buy/c-1f4/#bread']         #油电混动


def get_parent_text(element):
    parent_text = element.text
    for child_element in element.find_elements_by_xpath(".//*"):
        parent_text = parent_text.replace(child_element.text,'')
    return parent_text



def load_driver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("permissions.default.image",2)
    
    driver = webdriver.Firefox(firefox_profile=profile)
    #driver.get("https://www.guazi.com/www/buy/c-1f3/#bread")
               
    return driver

def get_car_link(driver,vehicle_type): 
    today = str(date.today())
    page = 0
    
    file_location = 'C:/Users/Lenovo/Desktop/selenium/selenium/All_Vehicle/output-%s.csv' % today
    columns=['info','vehicle_id','link','record_date','vehicle_type']
                
    if not os.path.isfile(file_location):
        df = pd.DataFrame(columns=columns)
    else:
        df = pd.read_csv(file_location,encoding='gbk')
    
    try:
        while driver.find_element_by_partial_link_text('下一页') != None:
            
            car_list = driver.find_element_by_class_name('carlist')
            li_list = car_list.find_elements_by_xpath('./li')

            for li in li_list:
                info = li.text.replace('\n','').replace('\r','')
                vehicle_id = li.get_attribute('data-scroll-track')
                link = li.find_element_by_class_name('car-a').get_attribute('href')
                          
                new_df = pd.DataFrame(columns=columns,
                                        data=[[info,vehicle_id,link,today,vehicle_type]])
            
                df = df.append(new_df)
                
            next_page = driver.find_element_by_partial_link_text('下一页')
            next_page.click()
            page = page + 1
            print(page)
            time.sleep(2)
            
            df.to_csv(file_location,index=False)
    except:
        pass

def run_link_list(link_list,driver):
    for link in link_list:
        time.sleep(5)
        driver.get(link)
        try:
            title = driver.find_element_by_class_name('titlebox')
            title_data = get_parent_text(title)
            
            car_number = driver.find_element_by_class_name('right-carnumber')
            car_number_data = get_parent_text(car_number)
            car_number_data = car_number_data.replace('\n','').replace('车源号：','')
            
            price = driver.find_element_by_class_name('pricestype')
            price_data = get_parent_text(price)
            
            
            new_car_price = driver.find_element_by_class_name('newcarprice')
            new_car_price_data = get_parent_text(new_car_price)
            
            licensing_time = driver.find_element_by_class_name('one')
            licensing_time_data = licensing_time.find_elements_by_xpath(".//*")[0].text
            
            miles = driver.find_element_by_class_name('two')
            miles_data = miles.find_elements_by_xpath(".//*")[0].text
            
            license_location = driver.find_element_by_class_name('three')
            license_location_data = license_location.find_elements_by_xpath(".//*")[0].text
            
            make_data = driver.find_elements_by_xpath("//tr[* = '厂商']/self::tr")[0].text.replace('厂商 ','')
            type_data = driver.find_elements_by_xpath("//tr[* = '级别']/self::tr")[0].text.replace('级别 ','')
            battery_volume_data = driver.find_elements_by_xpath("//tr[* = '电池容量(kWh)']/self::tr")[0].text.replace('电池容量(kWh) ','')
            battery_power_data = driver.find_elements_by_xpath("//tr[* = '电动机总功率(kW)']/self::tr")[0].text.replace('电动机总功率(kW) ','')
            battery_torque_data = driver.find_elements_by_xpath("//tr[* = '电动机总扭矩(N·m)']/self::tr")[0].text.replace('电动机总扭矩(N·m) ','')
            endurance_miles_data = driver.find_elements_by_xpath("//tr[* = '续航里程(km)']/self::tr")[0].text.replace('续航里程(km) ','')
            
            today = str(date.today())
            
            if not os.path.isfile('C:/Users/Lenovo/Desktop/selenium/selenium/EV/output.csv'):
                df = pd.DataFrame(columns=['title','car_number','price','new_car_price','licensing_time','miles',
                                      'license_location','battery_volume','battery_power_data','battery_torque_data',
                                      'endurance_miles','make','type','record_date'])
            else:
                df = pd.read_csv('C:/Users/Lenovo/Desktop/selenium/selenium/EV/output.csv',encoding='gbk')
                
            
            new_df = pd.DataFrame(columns=['title','car_number','price','new_car_price','licensing_time','miles',
                                      'license_location','battery_volume','battery_power_data','battery_torque_data',
                                      'endurance_miles','make','type','record_date'],
                                        data=[[title_data,car_number_data,price_data,new_car_price_data,
                                              licensing_time_data,miles_data,license_location_data,battery_volume_data,
                                              battery_power_data,battery_torque_data,endurance_miles_data,make_data,type_data,today]])
            
        
            df = df.append(new_df)
            print(len(df))
            df.to_csv('C:/Users/Lenovo/Desktop/selenium/selenium/EV/output.csv',index=False)
            print(title_data)
        except:
            pass



driver = load_driver()
for i in l_list:
    driver.get(i[0])
    time.sleep(2)
    get_car_link(driver,i[1])