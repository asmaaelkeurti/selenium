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

def get_car_detail(driver):
    file_location = 'C:/Users/Lenovo/Desktop/selenium/selenium/All_Vehicle/record_detail.csv'
    columns=['licensing_time_data', 'miles_data', 'general_transmission_data', 'make_data', 'type_data', 'transmission_data',
             'engine_data', 'body_structure_data', 'length_width_height_data', 'wheelbase_data', 'total_mass_data',
             'backtrunk_size_data', 'displacement_data', 'intake_style_data', 'cylinder_data', 'housepower_data', 'gas_engine_torque_data',
             'fuel_type_data', 'electric_engine_type_data', 'battery_type_data', 'battery_volume_data', 'battery_power_data',
             'battery_torque_data', 'endurance_miles_data', 'vehicle_id', 'location', 'model']
    
    if not os.path.isfile(file_location):
        df = pd.DataFrame(columns=columns)
    else:
        df = pd.read_csv(file_location,encoding='gbk')
    
    recorded = pd.read_csv('C:/Users/Lenovo/Desktop/selenium/selenium/All_Vehicle/recorded.csv',encoding='gbk')
    
    for index,row in recorded[recorded['recorded'] == 0].iterrows():
        print(row['link'])
        driver.get(row['link'])
        time.sleep(2)
        vehicle_id = row['vehicle_id']
        location = row['location']
        model = row['model']
        
        licensing_time = driver.find_element_by_class_name('one')
        licensing_time_data = licensing_time.find_elements_by_xpath(".//*")[0].text
        
        miles = driver.find_element_by_class_name('two')
        miles_data = miles.find_elements_by_xpath(".//*")[0].text
        
        general_transmission = driver.find_element_by_class_name('last')
        general_transmission_data = general_transmission.find_elements_by_xpath(".//*")[0].text
        
        make_data = driver.find_elements_by_xpath("//tr[* = '厂商']/self::tr")[0].text.replace('厂商 ','')
        type_data = driver.find_elements_by_xpath("//tr[* = '级别']/self::tr")[0].text.replace('级别 ','')
        
        try:
            engine_data = driver.find_elements_by_xpath("//tr[* = '发动机']/self::tr")[0].text.replace('发动机 ','')
        except:
            engine_data = None
            
        try:
            displacement_data = driver.find_elements_by_xpath("//tr[* = '排量(L)']/self::tr")[0].text.replace('排量(L) ','')
        except:
            displacement_data = None
            
        try:
            intake_style_data = driver.find_elements_by_xpath("//tr[* = '进气形式']/self::tr")[0].text.replace('进气形式 ','')
        except:
            intake_style_data = None 
        
        try:
            cylinder_data = driver.find_elements_by_xpath("//tr[* = '气缸']/self::tr")[0].text.replace('气缸 ','')
        except:
            cylinder_data = None    
            
        try:
            housepower_data = driver.find_elements_by_xpath("//tr[* = '最大马力(Ps)']/self::tr")[0].text.replace('最大马力(Ps) ','')
        except:
            housepower_data = None 
            
        try:
            gas_engine_torque_data = driver.find_elements_by_xpath("//tr[* = '最大扭矩(N*m)']/self::tr")[0].text.replace('最大扭矩(N*m) ','')
        except:
            gas_engine_torque_data = None 
            
        try:
            fuel_type_data = driver.find_elements_by_xpath("//tr[* = '燃油标号']/self::tr")[0].text.replace('燃油标号 ','')
        except:
            fuel_type_data = None
        
        try:
            fuel_type_data = driver.find_elements_by_xpath("//tr[* = '排放标准']/self::tr")[0].text.replace('排放标准 ','')
        except:
            fuel_type_data = None
        
        try:
            electric_engine_type_data = driver.find_elements_by_xpath("//tr[* = '电机类型']/self::tr")[0].text.replace('电机类型 ','')
        except:
            electric_engine_type_data = None
        
        try:
            battery_type_data = driver.find_elements_by_xpath("//tr[* = '电池类型']/self::tr")[0].text.replace('电池类型 ','')
        except:
            battery_type_data = None
            
        try:
            battery_volume_data = driver.find_elements_by_xpath("//tr[* = '电池容量(kWh)']/self::tr")[0].text.replace('电池容量(kWh) ','')
        except:
            battery_volume_data = None
        
        try:
            battery_power_data = driver.find_elements_by_xpath("//tr[* = '电动机总功率(kW)']/self::tr")[0].text.replace('电动机总功率(kW) ','')
        except:
            battery_power_data = None
        
        try:
            battery_torque_data = driver.find_elements_by_xpath("//tr[* = '电动机总扭矩(N·m)']/self::tr")[0].text.replace('电动机总扭矩(N·m) ','')
        except:
            battery_torque_data = None    
            
        try:
            endurance_miles_data = driver.find_elements_by_xpath("//tr[* = '续航里程(km)']/self::tr")[0].text.replace('续航里程(km) ','')
        except:
            endurance_miles_data = None
        
        transmission_data = driver.find_elements_by_xpath("//tr[* = '变速箱']/self::tr")[0].text.replace('变速箱 ','')
        body_structure_data = driver.find_elements_by_xpath("//tr[* = '车身结构']/self::tr")[0].text.replace('车身结构 ','')
        length_width_height_data = driver.find_elements_by_xpath("//tr[* = '长*宽*高(mm)']/self::tr")[0].text.replace('长*宽*高(mm) ','')
        wheelbase_data = driver.find_elements_by_xpath("//tr[* = '轴距(mm)']/self::tr")[0].text.replace('轴距(mm) ','')
        total_mass_data = driver.find_elements_by_xpath("//tr[* = '整备质量(kg)']/self::tr")[0].text.replace('整备质量(kg) ','')
        backtrunk_size_data = driver.find_elements_by_xpath("//tr[* = '行李箱容积(L)']/self::tr")[0].text.replace('行李箱容积(L) ','')
    
        
        new_df = pd.DataFrame(columns=columns, data=[[licensing_time_data, miles_data, general_transmission_data, make_data, type_data, transmission_data,
                                                      engine_data, body_structure_data, length_width_height_data, wheelbase_data, total_mass_data,
                                                      backtrunk_size_data, displacement_data, intake_style_data, cylinder_data, housepower_data, gas_engine_torque_data,
                                                      fuel_type_data, electric_engine_type_data, battery_type_data, battery_volume_data, battery_power_data,
                                                      battery_torque_data, endurance_miles_data, vehicle_id, location, model]])
            
        df = df.append(new_df)
        df.to_csv(file_location,index=False)
    



def run_link_list_1(link_list,driver):
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



#driver = load_driver()
#for i in l_list:
#    driver.get(i[0])
#    time.sleep(2)
#    get_car_link(driver,i[1])