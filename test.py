from flask import Flask, request, jsonify
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
import urllib
app = Flask(__name__)
@app.route('/weather', methods=['POST']) # 날씨 정보 블럭에 스킬로 연결된 경로
def weather():
    req = request.get_json()
    params = req['action']['detailParams']
    if 'sys_location' not in params.keys(): # 입력 텍스트에 지역이 없을 경우는 바로 경고 메시지 전송
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "지역을 입력하세요."
                        }
                    }
                ]
            }
        }
        return jsonify(res)
    if 'sys_location' in params.keys(): # 지역을 시 구 동으로 3개까지 입력을 받을 수 있어서 순서대로 location에 저장
        location = params['sys_location']['value']
    if 'sys_location1' in params.keys():
        location += ' + ' + params['sys_location1']['value']
    if 'sys_location2' in params.keys():
        location += ' + ' + params['sys_location2']['value']
    location_encoding = urllib.parse.quote(location + '+날씨') # url 인코딩
    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%s'%(location_encoding)
    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find('span', {'class':'btn_select'})==None:    # 동일 시에 구만 다른 같은 이름의 동이 있을 경우
        region = soup.find('li', {'role' : 'option'}).text 
    else:
        region = soup.find('span', {'class':'btn_select'}).text
    if 'sys_date_period' in params.keys(): 
        weekly_weather = soup.find_all('li', {'class':'date_info today'})
    elif 'sys_date' not in params.keys() or 'today' in params['sys_date']['value']: # 오늘 미세먼지 가져오기
        info = soup.find('p', {'class': 'cast_txt'}).text
        temp_rain_info = soup.find_all('dd', {'class':'weather_item _dotWrapper'})
        temp = temp_rain_info[0].text.replace('도','')
        rain_rate = temp_rain_info[8].text
        sub_info = soup.find_all('dd')
        finedust = sub_info[2].text.replace('㎍/㎥', '㎍/㎥ ')
        Ultrafinedust = sub_info[3].text.replace('㎍/㎥', '㎍/㎥ ')
        if int(finedust[0:2]) > 31:
            answer = '%s 현재 미세먼지 정보입니다.\n\n' %(region)
            answer += '미세먼지 : ' + finedust + '\n'
            answer += '초미세먼지 : ' + Ultrafinedust + '\n' + '\n'
            answer += '양집사의 코멘트: 마스크 착용을 권장합니다!😷' + '\n' + '\n'
            answer += '전 단계로 돌아가고 싶으시면 "ㅎㅇ"를 입력해 주세요! 👈'
        else:
            answer = '%s 현재 미세먼지 정보입니다.\n\n' %(region)
            answer += '미세먼지 : ' + finedust + '\n'
            answer += '초미세먼지 : ' + Ultrafinedust + '\n' + '\n'
            answer += '양집사의 코멘트: 미세먼지가 낮습니다. 마스크 착용을 하지 않으셔도 되겠네요.😊' + '\n' + '\n'
            answer += '전 단계로 돌아가고 싶으시면 "ㅎㅇ"를 입력해 주세요! 👈'
    elif 'tomorrow' in params['sys_date']['value']: # 내일 날씨를 요청했을 경우
        def convert(text):
            text = text.split(' ')
            return ' '.join(text).split()
        tomorrow = soup.find_all('li', {'class':'date_info today'})[1].text
        tomorrow = convert(tomorrow)
        info = soup.find('div', {'class':'tomorrow_area _mainTabContent'})
        cast = info.find_all('div', {'class':'info_data'})
        answer = '%s 내일 기상정보입니다.\n\n' %(region)
        answer += '기온 : ' + tomorrow[-1] + '\n'
        answer += '기상 : ' + convert(cast[0].text)[0] + '/' + convert(cast[1].text)[0] + '\n'
        answer += '강수확률 : ' + tomorrow[3] + '/' + tomorrow[5] + '\n'
        answer += '미세먼지 : ' + convert(cast[0].text)[-1] + '/' + convert(cast[1].text)[-1]
    # 일반 텍스트형 응답용 메시지
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }
    return jsonify(res)
@app.route('/vancouvertime', methods=['POST']) # 캐나다 벤쿠버 시간 정보 블럭에 스킬로 연결된 경로
def vancouvertime():
   req = request.get_json()
   location2 = req["action"]["detailParams"]
   url = 'https://search.yahoo.com/search?p=vancouver+time&fr=yfp-t&ei=UTF-8&fp=1'
   #enc_loc = urllib.parse.quote(location2 + '+ 시간')
   #el = str(enc_loc)
   #url = 'https://search.yahoo.com/search?p='
   #url = url + el
   #url = url + '&fr=yfp-t&ei=UTF-8&fp=1'
   req = Request(url)
   page = urlopen(req)
   html = page.read()
   soup = BeautifulSoup(html, 'html.parser')
   r1 = soup.find('div', class_='compTitle d-ib mt-16 va-mid')
   r2 = r1.find('h3', class_='title')
   r3 = r2.find('span', class_='fc-inkwell fz-32 lh-40 primaryCityTime').text
   ampm = str(r3[6:8])
   hour = str(r3[0:2])
   minute = str(r3[3:5])
   global answer
   answer = ''
   if ampm == 'AM':
       answer += '현재 캐나다 벤쿠버의 시간은 오전 ' + hour + '시 ' + minute + '분입니다.' + '\n' + '\n' 
       if int(hour) < 6:
           answer += '양집사의 코멘트: 지금은 자는 시간이에요! 🌙'
       else:
           answer += '양집사의 코멘트: 하루 업무가 시작되는 상쾌한 아침입니다. ☀'
       answer += '\n' + '\n'
       answer += '전 단계로 돌아가고 싶으시면 "ㅎㅇ"를 입력해 주세요! 👈'
   else:
       answer += '현재 캐나다 벤쿠버의 시간은 오후 ' + hour + '시 ' + minute + '분입니다.' + '\n' + '\n' 
       if int(hour) < 19:
           answer += '양집사의 코멘트: 점심을 먹고 업무가 조금씩 마무리되는 오후입니다. ☀'
       else:
           answer += '양집사의 코멘트: 밤이 되었습니다. 하루 일과가 거의 마무리되는 시간입니다. 🌙'
       answer += '\n' + '\n'
       answer += '전 단계로 돌아가고 싶으시면 "ㅎㅇ"를 입력해 주세요! 👈'
   res = {
       "version": "2.0",
       "template": {
           "outputs": [
               {
                   "simpleText": {
                       "text": answer
                   }
               }
           ]
       }
   }
   return jsonify(res)
@app.route('/stock', methods=['POST']) # 한국 주식 정보 블럭에 스킬로 연결된 경로
def stock():
    req = request.get_json()
    company = req["action"]["detailParams"]["sys_text"]["value"]
    enc_com = urllib.parse.quote(company + '+ 주식')
    com = str(enc_com)
    url = 'https://m.search.naver.com/search.naver'
    url = url + '?sm=mtp_hty.top&where=m&query='
    url = url + com
    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html, 'html.parser')
    r1 = soup.find('div', class_='stock_price')
    r2 = r1.find('strong', class_='price').text
    if 1 > 0:
        answer = company + "의 현재 가격은 " + r2 + "원 입니다. 성투 하세요!" + '\n' + '\n'
        answer += '전 단계로 돌아가고 싶으시면 "ㅎㅇ"를 입력해 주세요! 👈'
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }
    return jsonify(res)
# 메인 함수
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)