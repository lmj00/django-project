## 주제
- 위치 기반 중고 거래


## 알게된 점
- 웹에서는 geolocation으로 사용자의 IP로 위치를 찾기 때문에 정확성이 떨어진다. 따라서 위치기반은 웹보다는 GPS가 있는 모바일 서비스에 적합하다.
- 거리는 위도와 경도를 통해 계산된다.
- 채팅은 소켓을 통해서 구현된다. 


## 아쉬운 점
- 처음부터 시작한 게 아닌, 기존 코드잇 템플릿을 사용해서 채팅과 거리 조절 기능을 추가했다.
- ERD 설계를 하지 않고 프로젝트를 시작하여 채팅을 구현하는 과정에서 많은 시간을 소요했다.  
- Django channels를 완벽히 이해하지 않고 기능 구현을 했다.


## 보완할 점
- 이미지를 S3에 업로드 했지만, 이미지의 삭제와 수정을 연동하지 않았다.
- 채팅방을 구매자와 판매자로 생성했기 때문에, 판매자가 동일한 물품으로 채팅을 시작하면 이전의 채팅방으로 연결된다.
- 채팅방에서 새로운 채팅이 온 것을 setInterval로 0.5초 간격으로 확인했는데, 다른 방법이 있는지 확인이 필요할 것 같다.


## 기간
- 2022.03~2022.11


## 팀원
- 이수호(프론트엔드)
- 이민진(백엔드)


## 사용 기술
- Django, Django Channels, haversine


## 주요 기능
- 회원가입 시 주소 선택
- csv 파일로 db에 20551개의 법정동 데이터를 넣어 유효성 검사
![image](https://user-images.githubusercontent.com/54443194/222471244-3bca2f93-092d-4ded-adad-0b1f5cfb7ab7.png)

<br>

- 거리 조절
![image](https://user-images.githubusercontent.com/54443194/224852596-7695614d-55c3-41c1-bba3-8c8fb48c8882.png)

- (서울 성동구 행당동)의 아이디로 거리 조절을 했을 때
![image](https://user-images.githubusercontent.com/54443194/224852869-99ae8995-5baf-4dff-b14b-58c78d8ecccc.png)

<br>

- 채팅
![image](https://user-images.githubusercontent.com/54443194/222528286-9ac5d4c6-ec49-4eb1-947e-d39f753f61e1.png)
