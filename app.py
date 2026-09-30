# 배치 공정 이상탐지 — 품질 의사결정 지원 대시보드

## 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

기본 주소는 http://localhost:8501 입니다.

## 폴더 구성

```
app/
├── app.py                      Streamlit 앱
├── requirements.txt
└── artifacts/
    ├── model_v3.joblib         RF · PCA · 스케일러 · 관리한계 · 성능 지표
    ├── roc_curve.csv           운영점 환산용 ROC
    ├── feature_importance.csv  공정변수별 기여도
    ├── sensitivity.csv         민감도 분석 결과
    ├── model_summary.csv       모델 성능 요약
    ├── metrics.json            전체 지표
    ├── sample_normal.csv.gz    정상 Run 샘플
    └── sample_anomalous.csv.gz 이상 Run 샘플
```

## 탭 구성

| 탭 | 내용 |
|---|---|
| **배치 판정** | 윈도 특성 CSV 업로드 → 관리도 · 한계 대비 · 점검 후보 |
| **검증 결과** | 4단계 분할 · 모델 성능 · 민감도 분석 |
| **조기탐지 한계** | 대조군 교차 비교 · 사전 게이트 판정 |
| **조사 부하 설계** | 오탐률별 연간 건수 · 경보당 적중률 |
| **모델 정보** | 분석 규모 · 배치 단위 판정 · 적용 범위 |

## 판정 방식

배치 단위 판정 지표는 **시점별 SPE 의 상위 5% 분위수**다.
시점 단위 관리한계를 배치에 그대로 적용하면 정상 배치도 다수 초과하므로,
Run 단위로 요약한 뒤 정상 Run 분위수 기준의 관리한계와 비교한다.

| 지표 | Run 단위 AUROC |
|---|---|
| max | 0.870 |
| **q95 (채택)** | **0.854** |
| mean | 0.833 |
| median | 0.707 |

max 가 근소하게 높으나 단일 시점에 좌우되어 불안정하므로 q95 를 채택했다.

## 입력 데이터 형식

분석 노트북 PART 3 에서 생성한 윈도 특성 CSV 를 사용한다.
필수 컬럼은 `t_end` 와 186개 특성이며, 누락된 특성은 결측 처리된다.

## 적용 범위

- 본 시스템은 일탈(Deviation)을 **판정하지 않는다**
- 기여도는 인과가 아니라 **조사 우선순위 후보**다
- 실험실 규모 연구 데이터 기반이며 GMP 생산 기록이 아니다
- 원료 로트·설비 변경 시 기준선 재평가가 필요하다 (변경관리 대상)
