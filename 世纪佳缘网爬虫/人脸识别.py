#coding:utf-8
from aip import AipFace

""" 你的 APPID AK SK """
APP_ID = '10252502'
API_KEY = 'Ybsb43yXs8NLFXflQ0ySW7kE'
SECRET_KEY = '2WOEGA04PCwxommlcYk6O59XnSA344Ua'

aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)


# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 调用人脸属性检测接口
'''
result = aipFace.detect(get_file_content('face.jpg'))
print result
'''
# 定义参数变量
options = {

    'face_fields': "beauty",
}

# 调用人脸属性识别接口
for i in range(1,1000):
    result = aipFace.detect(get_file_content(r'F:\picture\\'+str(i)+".jpg"), options)
    try:
        print ("第"+str(i)+"张的颜值分:",result['result'][0]['beauty'])
    except IndexError:
        print("图片不清晰，请上传高清大图!!!")
