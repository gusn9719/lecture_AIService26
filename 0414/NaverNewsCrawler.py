import urllib.request
import urllib.parse
import json 
import pandas as pd
from time import sleep

class NaverNewsCrawler:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://openapi.naver.com/v1/search/news.json"
        self.start = 1
        self.display = 10

    def set_start(self, start):
        self.start = start
    
    def set_display(self, display):
        self.display = display
    
    def crawl_naver_news(self, keyword):

        # 인터넷 통신은 언제 끊길지 몰라서 try-except로 예외 처리를 항상 해줘야 함
        try:
            # 1. 키워드 변환: 한글은 서버가 못 읽을 수 있으니 url에서 안전한 형태로 인코딩 
            # urllib.parse 한글 검색어("인공지능")을 웹주소 형식으로 변환 해주는 역할
            encText = urllib.parse.quote(keyword)
            
            # 2. url 조립
            url = f"{self.base_url}?query={encText}&start={self.start}&display={self.display}"

            # 3. 요청 
            request = urllib.request.Request(url)

            # 4. 인증
            request.add_header("X-Naver-Client-Id", self.client_id)
            request.add_header("X-Naver-Client-Secret", self.client_secret)

            # 5. 접속 / 응답 
            response = urllib.request.urlopen(request)
            rescode = response.getcode() # 200 이면 정상, 400/500대면 오류

            if rescode == 200:
                response_body = response.read()
                # 6. 받은 데이터를 utf8로 바꾸고 그걸 다시 파이썬 딕셔너리로
                json_data = response_body.decode('utf-8')
                return json.loads(json_data)
            else:
                print(f"Error : {rescode}" )
                return None

        except Exception as e:
            print(f"Exception : {e}")
            print(f"호출 시도한 URL: {url}")
            return None
        
    def get_repeat_crawler(self, keyword, max_start=999):

        result_news = []

        while self.start <= max_start:
            crawled_data = self.crawl_naver_news(keyword)
            if crawled_data:
                print(f"crawling 성공: {self.start}")

                result_news.extend(crawled_data['items'])
                self.start += self.display

                # 너무 빨리 접근하면 차단하는 거 막으려구 0.3초
                sleep(0.3)
            else:
                print(f"crawling 실패: {self.start}")

        return result_news

    def save_to_csv(self, data_list, filename):
        if not data_list:
            print("저장할 데이터가 없습니다~")
            return
        
        data_df = pd.DataFrame(data_list)

        data_df.to_csv(filename, encoding="utf-8-sig", index=False) # 한글 깨지는거 막으려면 
        # 인덴스 = 펄스는 index_col=0이랑 같은 기능 그런데 그냥 무조건 첫번째 없에는게 아니라 Unnamed:0 이라는 이상한 컬럼 생기면 없애는거 

        print(f"[{filename}] 경로에 총 {len(data_list)}건 저장 완료")