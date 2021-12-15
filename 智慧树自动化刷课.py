from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import threading
import time


class Zhihuishu(object):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach',True)
    # 开发者模式
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #静音
    options.add_argument('--mute-audio')

    driver_path = r'D:\ChromeDriver\chromedriver.exe'

    def __init__(self,username,password):
        self.username = username
        self.password = password

        self.driver = webdriver.Chrome(executable_path = self.driver_path,
                                       options=self.options)
    #退出
    def exit_def(self):
        self.driver.quit()
        exit()

    #登录
    def login(self):
        url = 'https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin'
        self.driver.get(url)

        #Js代码输入
        self.driver.execute_script('document.getElementById("lUsername").value="{}"'.format(self.username))
        time.sleep(0.5)
        self.driver.execute_script('document.getElementById("lPassword").value="{}"'.format(self.password))
        time.sleep(0.5)
        # 定位到输入密码的输入框，然后模拟键盘进行回车登录
        self.driver.find_element_by_id('lPassword').send_keys(Keys.ENTER)

        #查看是否登录成功
        try:
            #显示等待，查看登录按钮是否还在当前页面，如果还在，就登录失败
            WebDriverWait(self.driver,3).until_not(
                EC.presence_of_element_located((By.XPATH,'//*[@id="f_sign_up"]/div/span')))
            print('登陆成功')
        except Exception:
            print('登陆失败')
            self.exit_def()

    #获取课程信息
    def get_course_info(self):
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located(
            (By.XPATH,"//div[@id='sharingClassed']/div[2]/ul")))
        try:
            #课程列表
            courses = self.driver.find_elements_by_xpath("//div[@id='sharingClassed']/div[2]/ul")
            index = 1
            for course in courses:
                #获取课程名称
                course_name = course.find_element_by_xpath(".//div[@class='courseName']").get_attribute('textContent')
                #获取学习进度
                course_progress = course.find_element_by_xpath(".//span[@class='processNum']").get_attribute('textContent')
                print(f'{index} 课程名称:{course_name}\n进度：{course_progress}')
                index += 1
        except:
            print('获取课程列表失败')
            self.exit_def()

    #选择课程并进入，关闭‘我知道了’，和‘学前必读’
    def into_course(self):
        num = input('请选择课程>>>')
        try:
            self.driver.find_element_by_xpath(f"//div[@id='sharingClassed']/div[2]/ul["+num+"]/div/dl/dt/div[1]").click()
        except:
            print('课程选择失败')
            self.into_course()

        WebDriverWait(self.driver,10).until(EC.presence_of_element_located(
            (By.XPATH,"//div[@class='el-dialog']/div[3]//button")))
        try:
            self.driver.find_element_by_xpath("//div[@class='el-dialog']/div[3]//button").click()
            print('关闭‘我知道了’成功')
        except:
            pass

        WebDriverWait(self.driver,10).until(EC.presence_of_element_located(
            (By.XPATH,"//i[@class='iconfont iconguanbi']")))

        try:
            self.driver.find_element_by_xpath("//i[@class='iconfont iconguanbi']").click()
            print('关闭‘学前必读’成功')
        except:
            print('关闭‘学前必读’失败')

    def ckeck_course(self):
        videos = self.driver.find_elements_by_xpath("//li[starts-with(@class,'clearfix video')]")
        len_videos = int(len(videos))

        finished_video_count = 0
        for video in videos:
            try:
                video.find_element_by_xpath(".//b[@class='fl time_icofinish']")
                finished_video_count += 1

            # 如果检测到没有看的视频，就去点击他
            except:
                print('检测到没看完的章节')
                time.sleep(2)
                click = video.find_element_by_xpath(".//div[@class='fl cataloguediv-c']/span")
                time.sleep(2)
                ActionChains(self.driver).click(click).perform()

            # 不管try有没有异常都查看一遍是否全部看完了，看完了返回课程列表,执行into_course函数，重新选择课程
            finally:
                if finished_video_count == len_videos:
                    print('本课程已全部学完')
                    self.driver.find_element_by_xpath("//div[@class='back']").click()
                    self.into_course()

    #获取总时间以及当前章节
    def get_time(self):
        try:
            print('-'*50)
            time.sleep(2)
            #这个视频总时间
            total_time = self.driver.find_element_by_xpath("//span[@class='duration']").get_attribute('textContent')
            #章节
            chapter = self.driver.find_element_by_xpath("//span[@id='lessonOrder']").get_attribute('textContent')

            print(f'正在观看{chapter},总时长:{total_time}')
        except:
            print('获取时间以及正在看的章节失败')




    #设置画面倍速
    def set(self):
        #画面设置为流畅
        try:
            time.sleep(2)
            #js切换
            self.driver.execute_script('document.querySelector\
            ("#vjs_container > div.controlsBar > div.definiBox > div > b.line1bq.switchLine").click()')
            print('画面设置为流畅-->成功')
        except:
            print('画面设置为流畅-->失败')

        #倍速设置为1.5倍
        try:
            time.sleep(2)
            #js切换
            self.driver.execute_script('document.querySelector\
            ("#vjs_container > div.controlsBar > div.speedBox >div > div.speedTab.speedTab15").click()')
            print('1.5倍速切换成功')
        except:
            print('1.5倍速切换失败')

    #检测习惯分
    def custon_points(self):
        print('正在检测习惯分')
        while True:
            time.sleep(5)
            try:
                WebDriverWait(self.driver, timeout=True, poll_frequency=5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[8]/div/div[1]/button'))).click()
                self.driver.execute_script('document.querySelector("#playButton").click()')  # 点击播放
                print("关闭习惯分提示成功")
            except:
                pass

    #检测弹窗
    def close_windows(self):
        print("弹窗检测中")
        while True:
            try:
                # 显示等待查找弹窗，有弹窗就点击第一个不管对错然后确定
                WebDriverWait(self.driver, timeout=True, poll_frequency=10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "topic-item"))).click()
                self.driver.find_element_by_xpath('/html/body/div[1]/div/div[7]/div/div[3]/span/div').click()  # 点击关闭
                time.sleep(2)
                self.driver.execute_script('document.querySelector("#playButton").click()')  # 点击播放
                print("关闭弹窗成功")
            except:
                pass

    #播放下一集
    def next(self):
        while True:
            time.sleep (10)  # 10秒检测一次
            # 获取总时间
            total_time = self.driver.find_element_by_xpath ('//*[@id="vjs_container"]/div[10]/div[4]/span[2]').get_attribute ('textContent')
            # 获取当前时间
            current_time = self.driver.find_element_by_xpath ('//*[@id="vjs_container"]/div[10]/div[4]/span[1]').get_attribute ('textContent')
            print ("\r当前时间：{}".format (current_time), end="", flush=True)
            # 如果总时间等于当前时间就是看完了，
            if current_time == total_time:
                print ('本节视频播放完成，正在播放下一节')
                try:
                    time.sleep(3)
                    # 检查视频状态找下一个没有看完的视频
                    self.ckeck_course()
                    # 找到后进行画质倍速的设置
                    self.set ()
                    # 获取章节总时间
                    self.get_time ()
                except:
                    print ("点击下一节失败")

    def start_thread(self):
        custom = threading.Thread(target=self.custon_points)
        poput = threading.Thread(target=self.close_windows)
        next = threading.Thread(target=self.next)
        # 开始检测习惯分
        custom.start()
        # 开始检测弹窗
        poput.start()
        # 开始检测下一节
        next.start()

    def run(self):
        #登录
        self.login()
        #查看课程信息
        self.get_course_info()
        #选择并进入课堂 ：需要用户自己输入
        self.into_course()
        #查看视频状态
        self.ckeck_course()
        #获取正在观看的视频章节及总时长
        self.get_time()
        #设置画面和倍速
        self.set()
        #启动线程
        self.start_thread()

def main():
    username = input('please input your username>>>')
    password = input('please input your password>>>')
    spider = Zhihuishu(username,password)
    spider.run()


if __name__ == '__main__':
    main()
