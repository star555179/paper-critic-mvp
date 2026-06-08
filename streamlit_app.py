import streamlit as st
import random
from datetime import datetime

# 页面配置
st.set_page_config(page_title="论文智评 - 科研论文批判性阅读助手", page_icon="📄", layout="wide")

# 自定义CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #1E88E5; text-align: center; margin-bottom: 1rem; }
    .sub-header { font-size: 1.2rem; color: #555; text-align: center; margin-bottom: 2rem; }
    .question-card { background-color: #f8f9fa; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #1E88E5; }
    .confidence-high { color: green; font-weight: bold; }
    .confidence-mid { color: orange; font-weight: bold; }
    .confidence-low { color: red; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📄 论文智评 · MVP原型</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">基于多视角批判性思维引导的科研论文辅助阅读平台</div>', unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.markdown("## 🎯 关于本项目")
    st.markdown("""
    **论文智评** 为科研新手自动生成多视角批判性问题，并可视化论文论证结构。
    
    ### ✨ 三大创新点
    1. 多视角批判性问题生成（假设、实验、泛化、引用、伦理）
    2. 论点-证据知识图谱
    3. 置信度评分与可解释性
    """)
    st.caption(f"MVP版本 v1.0 | {datetime.now().strftime('%Y-%m-%d')}")

# 输入区
input_method = st.radio("选择输入方式", ["📄 上传PDF文件", "✍️ 粘贴论文文本"], horizontal=True)
paper_text = ""

if input_method == "📄 上传PDF文件":
    uploaded_file = st.file_uploader("请上传PDF格式的学术论文", type=["pdf"])
    if uploaded_file:
        try:
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages[:3]:
                paper_text += page.extract_text()
            st.success(f"✅ 成功提取 {len(paper_text)} 字符")
        except ImportError:
            st.warning("⚠️ 未安装PyPDF2，请改用粘贴文本方式")
        except Exception as e:
            st.error(f"PDF解析失败: {e}")
else:
    paper_text = st.text_area("请粘贴论文的摘要、引言或关键段落（至少200字）", height=200)

num_questions = st.slider("生成批判性问题数量", 3, 8, 5)
show_confidence = st.checkbox("显示置信度评分", value=True)
show_graph = st.checkbox("显示论证知识图谱", value=True)
analyze_btn = st.button("🚀 开始批判性分析", type="primary")

# 模拟生成函数
def generate_mock_questions(paper_text, num_q):
    templates = {
        "假设合理性": ["作者假设数据独立同分布，但真实场景中是否存在领域漂移？", "基线选择是否偏向本方法？未对比最新SOTA。"],
        "实验设计": ["评价指标是否全面？仅使用单一指标可能片面。", "消融实验是否充分？未单独验证每个模块贡献。"],
        "结论泛化性": ["结论能否推广到低资源场景？当前测试集与真实分布差异较大。", "模型在分布外数据上的表现未评估。"],
        "引用完整性": ["是否遗漏了2024-2025年的关键相关工作？", "核心贡献的支撑文献不足。"],
        "伦理风险": ["模型是否放大训练数据中的偏见？未进行公平性评估。", "数据隐私问题：数据集是否获得授权？"]
    }
    perspectives = list(templates.keys())
    questions = []
    for i in range(num_q):
        perspective = perspectives[i % len(perspectives)]
        text = random.choice(templates[perspective])
        confidence = round(random.uniform(0.55, 0.95), 2)
        questions.append({"perspective": perspective, "text": text, "confidence": confidence})
    return questions

if analyze_btn:
    if not paper_text.strip():
        st.error("❌ 请先上传PDF或粘贴论文文本。")
    else:
        with st.spinner("🔬 正在进行多视角批判性分析..."):
            import time; time.sleep(1.2)
            questions = generate_mock_questions(paper_text, num_questions)
        
        st.success("✅ 分析完成！")
        st.markdown("## 📌 创新点1：多视角批判性问题")
        for idx, q in enumerate(questions, 1):
            with st.container():
                st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([5,1])
                col1.markdown(f"**{idx}. [{q['perspective']}]** {q['text']}")
                if show_confidence:
                    conf = q['confidence']
                    if conf >= 0.8:
                        col2.markdown(f'<span class="confidence-high">🟢 置信度: {conf:.0%}</span>', unsafe_allow_html=True)
                    elif conf >= 0.6:
                        col2.markdown(f'<span class="confidence-mid">🟡 置信度: {conf:.0%}</span>', unsafe_allow_html=True)
                    else:
                        col2.markdown(f'<span class="confidence-low">🔴 置信度: {conf:.0%}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        if show_graph:
            st.markdown("## 🗺️ 创新点2：论证知识图谱（示例）")
            st.graphviz_chart("""
                digraph {
                    "假设: 数据独立同分布" -> "实验: 基准测试" -> "结论: 模型有效";
                    "假设" -> "局限: 未考虑领域漂移" [color=red];
                    "实验" -> "局限: 基线不全" [color=orange];
                }
            """)
        st.download_button("📥 下载结果", "\n\n".join([f"[{q['perspective']}] {q['text']}" for q in questions]), "critique.txt")
else:
    st.info("👆 请上传论文或粘贴文本，然后点击「开始批判性分析」体验功能。")
