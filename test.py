from selenium import webdriver
import pandas as pd
import time
import os.path

def get_parent_text(element):
    parent_text = element.text
    for child_element in element.find_elements_by_xpath(".//*"):
        parent_text = parent_text.replace(child_element.text,'')
    return parent_text



def load_driver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("permissions.default.image",2)
    
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get("https://www.guazi.com/www/buy/c-1f3/#bread")
               
    return driver

def get_car_link(driver): 
    link_list = []
    page = 0
    try:
        while driver.find_element_by_partial_link_text('下一页') != None:
            a_list = driver.find_elements_by_class_name('car-a')
            for a in a_list:
                link_list = link_list + [a.get_attribute('href')]
            next_page = driver.find_element_by_partial_link_text('下一页')
            next_page.click()
            page = page + 1
            print(page)
            print(len(link_list))
            time.sleep(5)
    except:
        pass
    return link_list

def run_link_list(link_list,driver):
    for link in link_list:
        time.sleep(5)
        driver.get(link)
        try:
            title = driver.find_element_by_class_name('titlebox')
            title_data = get_parent_text(title)
            
            car_number = driver.find_element_by_class_name('right-carnumber')
            car_number_data = get_parent_text(car_number)
            
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
            
            if not os.path.isfile('C:/Users/Lenovo/Desktop/selenium/output.csv'):
                df = pd.DataFrame(columns=['title','car_number','price','new_car_price','licensing_time','miles',
                                      'license_location','battery_volume','battery_power_data','battery_torque_data',
                                      'endurance_miles','make','type'])
            else:
                df = pd.read_csv('C:/Users/Lenovo/Desktop/selenium/output.csv',encoding='gbk')
                
            
            new_df = pd.DataFrame(columns=['title','car_number','price','new_car_price','licensing_time','miles',
                                      'license_location','battery_volume','battery_power_data','battery_torque_data',
                                      'endurance_miles','make','type'],
                                        data=[[title_data,car_number_data,price_data,new_car_price_data,
                                              licensing_time_data,miles_data,license_location_data,battery_volume_data,
                                              battery_power_data,battery_torque_data,endurance_miles_data,make_data,type_data]])
            
        
            df = df.append(new_df)
            print(len(df))
            df.to_csv('C:/Users/Lenovo/Desktop/selenium/output.csv',index=False)
            print(title_data)
        except:
            pass
