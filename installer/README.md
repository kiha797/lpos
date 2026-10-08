# MSI 설치 소스

이미 생성된 설치 파일은 ../dist/LabelPOS-Studio-Setup.msi 입니다.

payload/는 MSI 설치판 파일입니다. 웹 버전과 편집 기능은 같으며, 오프라인 설치 안내와 캐시 버전이 설치판용으로 적용되어 있습니다.

Linux에서 wixl·msitools를 설치한 뒤 이 폴더에서 `python3 build-msi.py`를 실행하면 MSI를 다시 빌드합니다. 생성 후 Windows 실기기에서 설치·실행·제거 및 프린터 출력 검증을 수행하세요. 디지털 서명은 포함되어 있지 않습니다.

첨부된 UniLabelDesigner 파일은 재사용·재배포하지 않았습니다.
