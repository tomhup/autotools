from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,os,cv2
import numpy as np

#  通过selenium方法，到达通讯录页面
def getweb(username,passwd):
    driver = webdriver.Firefox()

    driver.get("https://www.icloud.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "auth-frame")))
    driver.switch_to.frame(driver.find_element_by_id("auth-frame"))

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "account_name_text_field")))
    emailElement = driver.find_element(By.ID, 'account_name_text_field')
    emailElement.send_keys(username)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "sign-in")))
    sign_in = driver.find_element(By.ID, 'sign-in')
    sign_in.click()

    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "password_text_field")))
    emailElement = driver.find_element(By.ID, 'password_text_field')
    emailElement.click()
    emailElement.send_keys(passwd)

    driver.implicitly_wait(1)
    ss = driver.find_element(By.ID, 'sign-in')
    ss.click()

    driver.implicitly_wait(3)

    driver.get("https://www.icloud.com/#contacts")
    #driver.implicitly_wait(10)
    time.sleep(10)

    os.system('xdotool mousemove 100 300 click 1')
    time.sleep(1)
    os.system('xdotool key F12')
    time.sleep(5)
    my,mx=mathc_current_imt('Network.png')
    cmd = "xdotool mousemove %s %s click 1"%(mx[0],my[0])
    os.system(cmd)
    
    driver.refresh()

# 通过opencv.mathc_img方法，找到匹配图像的坐标
def mathc_img(image,Target,debug,value=0.7):
    img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(Target,0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = value
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7,249,151), 2)
    if debug:
        cv2.imshow('Detected',img_rgb)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    #print loc
    return loc

def mathc_current_imt(Target,value=0.7,debug=False):
    # 通过scrot命令获取全屏截图
    os.system('scrot all.png')
    loc=mathc_img('all.png',Target,value=value,debug=debug)
    return loc

#xrandr 1366x768
def getcurl():
    time.sleep(10)
    my,mx=mathc_current_imt('Network.png')
    # 通过xdotool命令操作鼠标和键盘
    cmd = "xdotool mousemove %s %s click 1"%(mx[0],my[0]+100)
    os.system(cmd)
    
    while True:
        my,mx = mathc_current_imt('t.png')
        if len(mx)>0 and len(my)>0:
            cmd = "xdotool mousemove %s %s click 3"%(mx[0],my[0])
            os.system(cmd)
            time.sleep(1)

            my,mx =mathc_current_imt('Copy.png')
            cmd = "xdotool mousemove %s %s click 3"%(mx[0],my[0])
            os.system(cmd)                          
            time.sleep(1)

            my,mx =mathc_current_imt('Copy_as_curl.png')
            cmd = "xdotool mousemove %s %s click 1"%(mx[0],my[0])
            os.system(cmd)    
            time.sleep(1)

            from pandas.util.clipboard import clipboard_get
            text = clipboard_get()
            cmd = text +' > data.json'
            os.system(cmd)
            
            break

        else:
            os.system("xdotool key Up")

if __name__ =='__main__':
    username= '*****'
    passwd = '*****'
    getweb(username,passwd)
    getcurl()
                      
