# LabelPOS Studio

라벨포스 전용 라벨 디자인 프로그램입니다.

- Windows 설치 파일: [LabelPOS-Studio-Setup.msi](dist/LabelPOS-Studio-Setup.msi) (GitHub 파일 화면에서 Download raw file 선택)
- ZIP 실행 패키지: [LabelPOS-Studio-Offline.zip](dist/LabelPOS-Studio-Offline.zip)
- 웹사이트 파일: `dist/`
- MSI 설치 소스: `installer/`

MSI 설치판은 Windows 10/11 64비트 기준이며, 설치 화면은 영문·편집 화면은 한글입니다. 실제 Windows 설치 및 프린터 출력 검증은 별도 필요합니다.


라벨포스 전용 웹 및 오프라인 라벨 디자이너. 앱은 dist/의 정적 HTML/CSS/JS로 구성되며 외부 CDN, API 또는 네트워크 의존성이 없다.

- 검증: `npm ci` 후 `npm run verify`
- 배포: dist/를 HTTPS 정적 사이트로 제공한다.
- Windows: offline/의 설치·실행 스크립트와 dist/를 배포 패키지로 구성한다.
- 패키지 갱신: `python scripts/package-offline.py`
- PWA 파일 변경 시 sw.js와 app.js의 캐시 버전을 함께 변경한다.
- 브라우저와 Windows 설치 버전의 저장 공간은 다르다. .lpos 파일을 사용해 이동한다.
- 현재 버전의 구현 범위 및 미지원 항목은 FEATURE-COMPARISON.md 참조.
- Windows 실기기 및 실제 프린터 검증은 별도 수행이 필요하다.

## 검증 범위

DOM 환경과 실제 캔버스 엔진에서 바코드 PNG 생성, 반복 렌더링, 텍스트 측정/줄바꿈, mm 용지 설정, 파일 복원, 실행 취소/다시 실행, 데이터 바인딩, 출력 수량/범위, 잘못된 값 검사, 일련번호, 레이어/그룹/잠금, 모든 템플릿 SVG, 가져오기 검증, XLSX 한글 왕복, A4 페이지 배치, 롤 페이지 크기를 확인했다.

브라우저의 실제 인쇄 창, PWA 설치 UI, Windows PowerShell 스크립트, 실제 바코드 스캐너 및 프린터 하드웨어는 이 환경에서 실행 검증하지 않았다.
