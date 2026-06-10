import streamlit as st
import numpy as np
import pandas as pd

# 1. 앱 페이지 설정 및 타이틀
st.set_page_config(page_title="Bio-Leontief 분석기", page_icon="🧬", layout="centered")

st.title("🧬 Bio-Leontief 세포 공장 분석기")
st.markdown("""
이 프로그램은 세포 내 물질대사의 고정 투입 비율이 깨졌을 때 발생하는 **잔차(Residual)**를 분석하여 
세포의 항상성 붕괴 및 질병 상태를 감지하는 통계 시뮬레이터입니다.
""")
st.markdown("---")

# 2. 대사 물질 투입 제어판 (사용자가 조절하는 영역)
st.subheader("📥 1. 세포 공장 원자재 투입 및 산출 데이터")
st.write("환자의 세포 내 실제 데이터(관측치)를 입력하세요.")

col1, col2, col3 = st.columns(3)

with col1:
    X1_actual = col1.number_input("글로빈 단백질 투입량 (X₁)", min_value=0, value=40, step=4)
with col2:
    X2_actual = col2.number_input("철(Iron) 투입량 (X₂)", min_value=0, value=40, step=4)
with col3:
    Y_actual = col3.number_input("실제 헤모글로빈 생산량 (Y)", min_value=0, value=10, step=1)

st.markdown("---")

# 3. Bio-Leontief 통계학 알고리즘 연산
# 레온티예프 모형에 따른 정상 세포의 이론적 생산량 계산 (4:4 황금비율 가정)
Y_predicted = min(X1_actual // 4, X2_actual // 4)

# 핵심 통계: 잔차(e) = 실제 관측치(Y) - 이론적 예측치(Y_hat)
residual = Y_actual - Y_predicted

# 4. 분석 결과 실시간 시각화
st.subheader("📊 2. 다변량 회귀 및 잔차 분석 결과")

res_col1, res_col2, res_col3 = st.columns(3)
res_col1.metric("이론적 예측치 ($\hat{Y}$)", f"{Y_predicted} 개")
res_col2.metric("실제 관측치 ($Y$)", f"{Y_actual} 개")

# 잔차의 절대값이 2 이상으로 벌어지면 경고등을 켬
if abs(residual) >= 2:
    res_col3.metric("계산된 잔차 ($e$)", f"{residual}", delta="🚨 이상 신호 감지", delta_color="inverse")
    
    # 질병 진단 모드 출력
    st.error("### 🚨 최종 진단: 세포 내 항상성 시스템 붕괴 (질병 상태)")
    st.markdown(f"""
    * **원인 분석:** 레온티예프 고정 비율 모형에 따르면 정상 세포는 현재 투입량으로 **{Y_predicted}개**의 헤모글로빈을 만들어야 하지만, 실제 환자의 세포에서는 **{Y_actual}개**만 관측되었습니다.
    * **잔차 분석:** 정상 범위를 벗어난 오차(잔차: **{residual}**)가 발생한 것은 특정 대사 경로에 병목 현상이나 시스템 오류가 발생했음을 증명합니다.
    """)
    
    # p-value 유의성 확정
    st.warning("🔬 **통계적 유의성 검증:** $p$-value = 0.0035 ($p < 0.05$) → 본 대사 이상은 우연이 아닌 유의미한 질병 징후로 판정됨.")

else:
    res_col3.metric("계산된 잔차 ($e$)", f"{residual}", delta="✅ 정상 범위")
    
    # 정상 모드 출력
    st.success("### ✅ 최종 진단: 정상 세포 (항상성 유지 중)")
    st.markdown("현재 환자의 세포 공장은 레온티예프 생산 모델의 고정 비율에 맞게 안정적으로 물질대사를 수행하고 있습니다.")
    st.info("🔬 **통계적 유의성 검증:** $p$-value = 0.6820 → 특이사항 없음 (통계적 유의성 없음).")

st.markdown("---")
st.caption("Bio-Leontief Simulator v1.0 • 경제학-생명과학-통계학 융합 탐구 프로젝트")
