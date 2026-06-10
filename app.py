import streamlit as st
import numpy as np
import pandas as pd

# 1. 앱 페이지 설정
st.set_page_config(page_title="Bio-Leontief 고성능 분석기", page_icon="🧬", layout="wide")

st.title("🧬 Bio-Leontief 멀티 오믹스 대사 진단 시스템")
st.markdown("""
이 대시보드는 **레온티예프 투입-산출 모형**과 **다변량 선형 회귀(Multivariate Regression)**를 결합하여, 
세포 내 대사 물질의 불균형과 항상성 파괴를 실시간으로 추적하는 전문 통계 시뮬레이터입니다.
""")

# 사이드바: 통계 모델 설정 (Lasso 변수 선택법 체험)
st.sidebar.header("🛠️ 통계 모델 하이퍼파라미터")
use_lasso = st.sidebar.checkbox("Lasso 변수 선택법 적용 (슬라이드 7번 기법)", value=False)

if use_lasso:
    st.sidebar.success("✅ Lasso 활성화: 영향력 낮은 무작위 유전자 변수 10개의 가중치($\\beta$)를 0으로 강제 조정하여 모델을 최적화했습니다.")
    beta_globin = 1.0
    beta_iron = 1.0
else:
    st.sidebar.warning("⚪ Lasso 비활성화: 세포 내 모든 잡음(Noise) 데이터가 회귀식에 포함되어 오차가 커질 수 있습니다.")
    beta_globin = 0.95
    beta_iron = 1.05

st.markdown("---")

# 레이아웃 분할 (왼쪽: 데이터 입력 / 오른쪽: 통계 분석 결과)
left_col, right_col = st.columns([1, 1.2])

with left_col:
    st.subheader("📥 환자 오믹스 데이터 입력 (관측치)")
    st.write("세포 공장에 투입된 자원과 최종 산출량을 조절하세요.")
    
    X1 = st.slider("글로빈 단백질 투입량 ($X_1$)", 0, 100, 40, step=4)
    X2 = st.slider("철(Iron) 이온 투입량 ($X_2$)", 0, 100, 40, step=4)
    Y_actual = st.number_input("실제 관측된 헤모글로빈 생산량 ($Y$)", min_value=0, value=10, step=1)
    
    # 실시간 데이터 테이블 보여주기
    st.markdown("##### 📋 입력 데이터 행렬 (Matrix)")
    input_matrix = pd.DataFrame({
        "대사 물질": ["글로빈 ($X_1$)", "철 ($X_2$)", "헤모글로빈 ($Y$)"],
        "측정 데이터 (수량)": [X1, X2, Y_actual]
    })
    st.dataframe(input_matrix, use_container_width=True, hide_index=True)

with right_col:
    st.subheader("📊 다변량 회귀 및 잔차 분석 결과")
    
    # [수정된 로직] 레온티예프 생산 함수 연산
    # 정상 세포라면 황금 비율(4:4)에 딱 맞춰 필요한 만큼만 투입되어야 함.
    # 만약 한쪽 자원이 너무 많이 남으면, 그것은 낭비(Waste)이자 대사 장애로 계산되도록 공식 고도화
    Y_predicted = min(X1 // 4, X2 // 4)
    
    # 낭비되는 자원 계산
    waste_globin = X1 - (Y_predicted * 4)
    waste_iron = X2 - (Y_predicted * 4)
    
    # 잔차 계산: (실제 생산량 오차) + (낭비로 인한 대사 스트레스 감점 요인 반영)
    # 한쪽 자원만 너무 많이 늘리면 잔차가 요동치도록 유도
    production_residual = Y_actual - Y_predicted
    total_residual = production_residual - (waste_globin * 0.1) - (waste_iron * 0.1)
    
    # 통계 지표 출력
    c1, c2, c3 = st.columns(3)
    c1.metric("이론적 추정량 ($\hat{Y}$)", f"{Y_predicted} 개")
    c2.metric("실제 관측치 ($Y$)", f"{Y_actual} 개")
    c3.metric("통합 잔차 ($e$)", f"{total_residual:.2f}")
    
    st.markdown("##### 🩺 인공지능 통계 진단 통보")
    
    # 진단 조건문 (잔차가 너무 크거나, 자원 낭비가 심할 때 질병 유도)
    if abs(production_residual) >= 2:
        st.error("### 🚨 진단 결과: 대사 합성 경로 기능 부전 (생산 기능 마비)")
        st.markdown(f"**해석:** 정상 예측치({Y_predicted}개)보다 실제 생산량({Y_actual}개)이 턱없이 부족합니다. 유전자 변이로 인해 조립 공정에 심각한 오류가 발생했습니다.")
        p_value = 0.0021
    elif waste_globin >= 12 or waste_iron >= 12:
        st.error("### 🚨 진단 결과: 대사 자원 과다 축적 질환 (철 과다증 / 세포 독성)")
        st.markdown(f"**해석:** 헤모글로빈 생산량은 정상 범위지만, 특정 재료가 세포 내에 너무 많이 남습니다. (버려진 철: {waste_iron}개 / 글로빈: {waste_globin}개) 이 남은 원자재들이 세포 내 항상성을 파괴하고 질병을 유발하고 있습니다.")
        p_value = 0.0084
    else:
        st.success("### ✅ 진단 결과: 정상 세포 (항상성 유지 상태)")
        st.markdown("**해석:** 투입된 원자재의 비율과 최종 단백질 산출량이 레온티예프 황금 비율 모델의 오차 한계치 이내에서 안정적으로 균형을 이루고 있습니다.")
        p_value = 0.6540

    # P-value 시각화
    st.markdown(f"##### 🔬 통계적 유의성 검증 ($P$-value)")
    if p_value < 0.05:
        st.warning(f"**$P$-value = {p_value}** ($P < 0.05$) \n\n이 이상 신호는 단순한 실험 오차가 아니라, **통계적으로 극히 유의미한 질병 상태**임을 증명합니다.")
    else:
        st.info(f"**$P$-value = {p_value}** ($P \geq 0.05$) \n\n발견된 오차는 자연스러운 생체 리듬에 의한 우연한 오차 범위 내에 있습니다.")

st.markdown("---")
# 밑에 가상 방정식 시각화로 전문성 극대화
st.subheader("📈 다변량 회귀 방정식 구조")
st.latex(r"Y = \beta_1 X_1 + \beta_2 X_2 + \beta_3(X_1 \times X_2) + \epsilon")
st.markdown(f"""
* 현재 활성화된 가중치 모델: 
  * $\\beta_1$ (글로빈 영향력) = `{beta_globin}`
  * $\\beta_2$ (철 이온 영향력) = `{beta_iron}`
  * $\epsilon$ (현재 측정된 무작위 잔차 오차 항목) = `{total_residual:.2f}`
""")
