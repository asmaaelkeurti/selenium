from selenium import webdriver

link_list = []
driver = webdriver.Firefox()
driver.get("https://www.guazi.com/www/buy/c-1f3/#bread")

page = 0
           
while driver.find_element_by_partial_link_text('下一页') != None:
    a_list = driver.find_elements_by_class_name('car-a')
    for a in a_list:
        link_list = link_list + [a.get_attribute('href')]
    next_page = driver.find_element_by_partial_link_text('下一页')
    next_page.click()
    page = page + 1
    print(page)
    print(len(link_list))


