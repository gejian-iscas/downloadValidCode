import base64
import urllib, sys, requests
import json
import os


def getBase64(fileName):
    with open(fileName, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        return 'data:image/jpeg;base64,%s'%s


def getValidCode(fileName):
    host = 'http://apigateway.jianjiaoshuju.com'
    path = '/api/v_1/yzmCustomized.html'
    method = 'POST'
    appcode = '126397076ACB93A14BBBB86F7B0A9F85'
    appKey = 'AKID9bc99cf25e8236895b3d1a31471e2f8f'
    appSecret = 'a862a43e954c8121e01bd6bddf35de53'
    querys = ''
    bodys = {}
    url = host + path
    v_pic = getBase64(fileName)
    bodys['v_pic'] = v_pic
    bodys['pri_id'] = 'ne4'
    post_data = urllib.parse.urlencode(bodys).encode('utf-8')
    request = urllib.request.Request(url, post_data)
    request.add_header('appcode', appcode)
    request.add_header('appKey', appKey)
    request.add_header('appSecret', appSecret)

    request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read()
    if (content):
        print(content)
    return content
#s = getBase64('pics/0.jpg')
#print(s)
#getValidCode('pics/0.jpg')

def parseJson(jsonCode):
    jsonDic = json.loads(jsonCode)
    v_code = jsonDic['v_code']
    err_code = jsonDic['errCode']
    return v_code, err_code


def changeFileName(oldFile, newFile):
    path = 'pics/'
    os.rename(path+oldFile, path+newFile)
    print('Change file name from %s to %s, succeed.'%(oldFile, newFile))


def main():
    for i in range(100, 501):
        path = 'pics/'
        fileName = '%d.jpg' % i
        content = getValidCode(path + fileName)
        v_code, err_code = parseJson(content)
        #print(v_code, err_code)
        if err_code == 0:
            changeFileName(fileName, v_code + '.jpg')


if __name__ == '__main__':
    main()

