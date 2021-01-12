from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import re
 
 
# 转换单个文件，输入为文件绝对路径
def convert(file_name, output_folder):
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": output_folder}      #设置默认下载路径
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(100)                                #设定隐性等待超时时间
    driver.get('http://ocrmaker.com/')                         #ocr网址
    time.sleep(0.8)
    action = ActionChains(driver)
    action.move_by_offset(0, 0).click().perform()                    #点掉小程序码
    driver.find_element_by_id("imageFile").send_keys(file_name)      # 定位上传按钮，添加本地文件
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='btnStartOCR']/a").click()               #点击开始
    driver.find_element_by_xpath("//*[@id='sucOrErrMesgDiv']/button").click()      #等待转换完成
    driver.find_element_by_id("btnDownloadText").click()                           #点击下载
    time.sleep(2)
    driver.quit()


# 转换整个文件夹里的文件，输入为文件夹绝对路径
def convert_D(input_folder, output_folder):
    #获取文件夹中文件信息，并按名称排序
    path = input_folder
    path_list = os.listdir(path)
    path_list.sort(key=lambda x: int(x.split('.')[0]))
    for filename in path_list:
        print(input_folder + os.sep + filename)
        convert(input_folder + os.sep + filename, output_folder)


# 重命名转换后的文件
def rename(input_folder):
    # 获取该目录下所有文件，存入列表中
    path = input_folder
    fileList = os.listdir(path)
    for fname in fileList:
        # 设置旧文件名（就是路径+文件名）
        oldname = path + os.sep + fname  # os.sep添加系统分隔符
        # 设置新文件名
        new_fname = re.sub("^ParsedResult \(", "", fname)  # 删除文件名中以w开头空格结束的子字符串
        new_fnames = re.sub("\)", "", new_fname)  # 删除文件名中以w开头空格结束的子字符串
        newname = path + os.sep + new_fnames
        if new_fnames == fname:
            continue
        os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
        print(oldname, '======>', newname)



convert_D('D:\\image', 'D:\\Download\\ocr')                   #输入文件夹，输出文件夹,注意格式
rename('D:\\\\Download\\\\ocr')                                #重命名为1，2，3...