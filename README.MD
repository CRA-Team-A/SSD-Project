팀명: Agile - 민첩하고 유기적인 팀이 되자!!!

팀장: 박상현

팀원: 김정원, 서지웅, 이원희, 최한비, 허은지 

Ground Rule
1. commit convention 따르기
2. 퇴근 시간 = 5시 준수
3. 4시 반 PR은 내일로 미루기
4. PR은 컴팩트(100 line 이하)하게 PR하기
5. 2인 이상 approve받고 merge requester가 직접 merge하기
6. review할 때 칭찬 하나 이상 + 웃는 이모티콘 꼭 1개 포함하기
7. 의견충돌시 다수결로 결정
8. PR하고 다른 티원에게 디스코드 등으로 알리기
9. PR은 최대한 올라온 순서대로 처리하기

Commit Convention
1. Commit 메시지 구조 
type : comment
2. type
   1) FEAT: 새로운 기능 추가
   2) FIX: 버그 수정
   3) STYLE: 스타일 관련 기능(코드 포맷팅, 세미콜론 누락, 코드 자체의 변경이 없는 경우)
   4) REFACTOR: 코드 리팩토링
   5) TEST: 테스트 코드 추가
   6) CHORE: 빌드 업무 수정, 패키지 매니저 수정(ex .gitignore 수정 같은 경우)
3. comment
 제목은 최대 50글자가 넘지 않도록 하고 마침표 및 특수기호는 사용하지 않는다.
 영문으로 표기하는 경우 동사(원형)를 가장 앞에 두고 첫 글자는 대문자로 표기한다.(과거 시제를 사용하지 않는다.)
 제목은 개조식 구문으로 작성한다. --> 완전한 서술형 문장이 아니라, 간결하고 요점적인 서술을 의미.
     ex) Fixed --> Fix, Added --> Add, Modified --> Modify

Coding Convention
1. 기본은 PEP8
2. 클래스 내부 변수는 public으로 하되 getter, setter를 통해서 호출
3. 클래스 이름은 PascalCase 클래스 내부 메소드, 변수는 snake_case, 전역변수는 UPPER_SNAKE_CASE
4. 리스트 타입은 변수명에 s를 붙여서 구분
5. 삼항연산자는 사용 X
6. 주석 사용 X
7. 브랜치 생성 룰: 미정
8. 메소드 & 함수는 동사로, 변수는 명사형
9. 메소드 & 함수 정의할 때, arguments, return value의 타입 명시
