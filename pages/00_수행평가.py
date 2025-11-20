import streamlit as st
import pandas as pd
import plotly.express as px

# ---- 데이터 불러오기 ----
df = pd.read_csv("chocolate.csv")

# cocoa_percent 숫자로 변환
df["cocoa_percent_num"] = df["cocoa_percent"].str.replace("%", "").astype(float)

# ---- UI 구성 ----
st.title("🍫 초콜릿 국가별 코코아 비율 분석 대시보드")
st.write("국가를 선택하면 해당 국가 원두로 만든 초콜릿들의 코코아 비율을 비교해볼 수 있어요!")

countries = sorted(df["country_of_bean_origin"].unique())

selected_country = st.selectbox("📍 국가 선택", countries)

filtered = df[df["country_of_bean_origin"] == selected_country]

st.subheader(f"🌍 {selected_country}의 초콜릿 코코아 함량 비교")

# ---- 색상 설정 (1등 = 빨강 / 나머지 = 그라데이션) ----
filtered_sorted = filtered.sort_values("cocoa_percent_num", ascending=False)

# 색상 리스트 생성 (1등은 빨강, 나머지는 연한 빨강 → 진한 빨강 그라데이션)
colors = ["red"]  # 1등 빨간색
gradient_colors = px.colors.sequential.Reds[len(filtered_sorted)-1:]  # 나머지 색
colors.extend(gradient_colors)

# ---- Plotly Bar Chart ----
fig = px.bar(
    filtered_sorted,
    x="specific_bean_origin_or_bar_name",
    y="cocoa_percent_num",
    title=f"{selected_country} 원두 초콜릿의 코코아 비율",
    color=filtered_sorted.index,  # 색 적용을 위한 index 사용
    color_discrete_sequence=colors
)

fig.update_layout(
    xaxis_title="초콜릿(원두/바 이름)",
    yaxis_title="코코아 비율 (%)",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

