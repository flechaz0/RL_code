import requests
import sys
import m3u8
import time
import os

client = requests.Session()
# 循环下载ts视频
class VideoCrawler():

    def __init__(self, url):

        super(VideoCrawler, self).__init__()
        self.url = url
        self.final_path = r"E:\Download\Film"

    # 下载并解析m3u8文件
    def get_url_from_m3u8(self, readAdr):

        with open('temp.m3u8', 'wb') as file:
            file.write(requests.get(readAdr).content)
        m3u8Obj = m3u8.load('temp.m3u8')

        return m3u8Obj.segments

    def run(self):
        print("Start!")
        start_time = time.time()
        realAdr = self.url  # m3u8下载地址
        urlList = self.get_url_from_m3u8(realAdr)  # 解析m3u8文件，获取下载地址
        urlRoot = self.url[0:self.url.rindex('/')]
        i = 1
        outputfile = open(os.path.join(self.final_path, '%s.ts' % self.fileName),
                          'wb')  # 初始创建一个ts文件，之后每次循环将ts片段的文件流写入此文件中从而不需要在去合并ts文件

        for url in urlList:
            try:
                download_path = "%s/%s" % (urlRoot, url.uri)  # 拼接地址
                resp = client.get(download_path)  # 使用拼接地址去爬取数据
                outputfile.write(resp.content)  # 将爬取到ts片段的文件流写入刚开始创建的ts文件中
                sys.stdout.write('\r正在下载：{}'.format(self.fileName))  # 通过百分比显示下载进度
                sys.stdout.flush()  # 通过此方法将上一行代码刷新，控制台只保留一行
            except Exception as e:
                print("\n出现错误：%s", e.args)
                continue  # 出现错误跳出当前循环，继续下次循环
            i += 1
        outputfile.close()
        success = os.system(
            r'copy /b E:\Download\Film\{0}.ts E:\Download\Film\{0}.mp4'.format(self.fileName))  # ts转成mp4格式
        if (not success):
            os.remove(self.final_path + '\\' + self.fileName + ".ts")  # 删除ts和m3u8临时文件
            os.remove("temp.m3u8")


if __name__ == '__main__':
        f = open("m3u8.txt", 'r', encoding='utf-8')
        line = f.read().splitlines()
        for i in range(len(line)):
            m3u8_addr = line[i]
            crawler = VideoCrawler(m3u8_addr)
            crawler.fileName = str(i+2)
            crawler.run()

