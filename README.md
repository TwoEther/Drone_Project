<h1> Drone_Project </h1>
<h2> CISC-W 2022 Winter Academic Contest </h2>

<h3> Team </h3>
평택대학교

<h3> Stack </h3>
<ul>
 <li>🥀 Python</li>
 <li>💻 Django</li>
 <li>🎢 MySQL</li>
 <li>🔧 HTML, CSS, JS</li>
</ul>

<h3> 역할 </h3>
<ul>
 <li>주기현 : 컨트롤러 및 프론트엔드 개발 1명</li>
 <ul>
    <li>파이썬 GUI를 이용한 컨트롤러 개발</li>
    <li>웹 프론트엔드 개발</li>
 </ul>
 <li>이현일 : 암복호화 및 백엔드 개발 1명 </li>
 <ul>
    <li>Drone과 Python과의 Connection 담당</li>
    <li>MySQL 테이블 생성 및 데이터 처리</li>
    <li>Django Configuration</li>
 </ul>
</ul> 
<hr/>

<h3> 기간 </h3>
<ul>
 <li>2022.07 ~ 2022.11</li>
</ul> 
<hr/>

<h3> 수상 </h3>
<strong>🥉 한국인터넷진흥원 원장상 수상</strong>
<hr/>

<h3> 정리 </h3>
<p>
 본 프로젝트는 드론의 정보를 MySQL 서버에 암호화 하여 저장하는 정보관제센터와 이 정보를 복호화하여 활용하는 정보활용센터로 구성됩니다,
 이 과정을 Python, Django, MySQL 등을 사용하여 구현하였습니다.</p>
 
<h3> DB table </h3>
<p>enc_table</p>

<table border="1">
  <th>변수</th>
  <th>타입</th>
  <th>설명</th>

  <tr><!-- 1번째 줄 시작 -->
      <td>DID</td>
      <td><span style="color:red">Integer</span></td>
      <td>드론아이디</td>
  </tr>
  
  <tr><!-- 2번째 줄 시작 -->
      <td>TOT</td>
      <td><span style="color:red">Integer</span></td>
      <td>이륙후 출발시간</td>
  </tr>
  
  <tr><!-- 3번째 줄 시작 -->
      <td>Flight</td>
      <td><span style="color:red">Boolean</span></td>
      <td>이륙시 1, 착륙시 0</td>
  </tr>
  
  <tr><!-- 4번째 줄 시작 -->
      <td>landing</td>
      <td><span style="color:red">Boolean</span></td>
      <td>!Flight</td>
  </tr>
  
  <tr><!-- 5번째 줄 시작 -->
      <td>Temperature</td>
      <td><span style="color:red">Float</span></td>
      <td>온도</td>
  </tr>
  
  <tr><!-- 6번째 줄 시작 -->
      <td>Pressure</td>
      <td><span style="color:red">Float</span></td>
      <td>압력</td>
  </tr>
  
  <tr><!-- 7번째 줄 시작 -->
      <td>Altitude</td>
      <td><span style="color:red">Float</span></td>
      <td>고도</td>
  </tr>
  
  <tr><!-- 8번째 줄 시작 -->
      <td>RangeHeight</td>
      <td><span style="color:red">Float</span></td>
      <td>시중고도</td>
  </tr>
  
  <tr><!-- 9번째 줄 시작 -->
      <td>enc_key</td>
      <td><span style="color:red">varchar</span></td>
      <td>사전에 공유된 암호키</td>
  </tr>

 </table><hr>
<p>컨트롤러의 버튼을 통하여 드론 조작 가능</p>
<img width="80%" src="https://user-images.githubusercontent.com/101616106/206077173-e9bd7194-35fb-4b62-ab20-413f74b86165.PNG"/><hr>
<p>로그인 한 유저에 대해서만 드론에 접근 가능</p>
<img width="80%" src="https://user-images.githubusercontent.com/101616106/206077176-4acb235d-8206-4ffc-bcf2-e7c3dd9d0f5f.PNG"/><hr>
<p>복호화 하기 위해 .pem 파일 필요 (이는 사전에 공유된 키이다)</p>
<img width="80%" src="https://user-images.githubusercontent.com/101616106/206077160-7bf887cf-431e-461e-98ef-9ff5a585fdd9.PNG"/><hr>
<p>드론 정보를 시각화 해서 보여줌.</p>
<img width="80%" src="https://user-images.githubusercontent.com/101616106/206077170-80919cec-e2a6-4d28-84f2-9e14dcb4ca20.PNG"/>
