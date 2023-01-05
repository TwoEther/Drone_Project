<h1> Drone_Project </h1>
<h2> CISC-W 2022 Winter Academic Contest </h2>

<h3> Team </h3>
PyeonTaekUniv.

<h3> Stack </h3>
<ul>
 <li>🥀 Python</li>
 <li>💻 Django</li>
 <li>🎢 MySQL</li>
 <li>🔧 HTML, CSS, JS</li>
</ul>

<h3> role </h3>
<ul>
 <li>컨트롤러 및 프론트엔드 개발 1명</li>
 <li>암복호화 및 백엔드 개발 1명 </li>
</ul> 
<hr/>

<h3> Awards </h3>
<strong>🥉 한국인터넷진흥원 원장상 수상</strong>
<hr/>

<h3> Summary </h3>
<p>
 본 프로젝트는 드론의 정보를 MySQL 서버에 암호화 하여 저장하는 정보관제센터와 이 정보를 복호화하여 활용하는 정보활용센터로 구성된다,
 이 과정을 Python, Django, MySQL 등을 사용하여 구현하였다.</p>
 
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
      <td></td>
  </tr>
  
  <tr><!-- 6번째 줄 시작 -->
      <td>Pressure</td>
      <td><span style="color:red">Float</span></td>
      <td></td>
  </tr>
  
  <tr><!-- 7번째 줄 시작 -->
      <td>Altitude</td>
      <td><span style="color:red">Float</span></td>
      <td></td>
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

 </table>
 <img width="80%" src="https://user-images.githubusercontent.com/101616106/206077173-e9bd7194-35fb-4b62-ab20-413f74b86165.PNG"/>
 <img width="80%" src="https://user-images.githubusercontent.com/101616106/206077176-4acb235d-8206-4ffc-bcf2-e7c3dd9d0f5f.PNG"/>
 <img width="80%" src="https://user-images.githubusercontent.com/101616106/206077160-7bf887cf-431e-461e-98ef-9ff5a585fdd9.PNG"/>
 <img width="80%" src="https://user-images.githubusercontent.com/101616106/206077170-80919cec-e2a6-4d28-84f2-9e14dcb4ca20.PNG"/>
