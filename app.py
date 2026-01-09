"""
🔬 Araştırma Ajanı - Streamlit Arayüzü
Kullanım: uv run streamlit run app.py
"""

import streamlit as st
from main import create_graph
from langchain_core.messages import HumanMessage

# ═══════════════════════════════════════════════════════════
#                    SAYFA AYARLARI
# ═══════════════════════════════════════════════════════════

st.set_page_config(
    page_title="🔬 Araştırma Ajanı",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════
#                       STİLLER
# ═══════════════════════════════════════════════════════════

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        font-size: 1.1rem;
        border-radius: 10px;
    }
    .stButton > button:hover {
        opacity: 0.9;
    }
    .result-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#                       BAŞLIK
# ═══════════════════════════════════════════════════════════

st.markdown('<p class="main-header">🔬 Araştırma Ajanı</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Araştırma Ajanını Hoşgeldiniz </p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#                    GİRİŞ ALANI
# ═══════════════════════════════════════════════════════════

col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    konu = st.text_input(
        "📌 Araştırmak istediğiniz konuyu yazın:",
        placeholder="Örnek: Mustafa Samet Karcık Kimdir ?",
        label_visibility="visible"
    )
    
    arastir_btn = st.button("🚀 Araştır", use_container_width=True)

# ═══════════════════════════════════════════════════════════
#                    ARAŞTIRMA İŞLEMİ
# ═══════════════════════════════════════════════════════════

if arastir_btn and konu:
    with st.spinner("🔍 Araştırma yapılıyor... Bu biraz zaman alabilir."):
        try:
            # Graf oluştur
            graph = create_graph()
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔍 Araştırmacı çalışıyor...")
            progress_bar.progress(25)
            
            # Ajanı çalıştır
            result = graph.invoke({
                "messages": [HumanMessage(content=konu)],
                "query": konu,
                "research_data": "",
                "summary": "",
                "revision_count": 0
            })
            
            progress_bar.progress(100)
            status_text.text("✅ Araştırma tamamlandı!")
            
            # Sonuçları göster
            st.markdown("---")
            st.markdown("### 📋 Araştırma Sonucu")
            
            # Özet
            st.markdown(result["summary"])
            
            # Meta bilgiler
            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("📝 Revizyon Sayısı", result["revision_count"])
            with col_b:
                st.metric("📏 Karakter Sayısı", len(result["summary"]))
                
        except Exception as e:
            st.error(f"❌ Hata oluştu: {str(e)}")

elif arastir_btn and not konu:
    st.warning("⚠️ Lütfen bir konu girin!")

# ═══════════════════════════════════════════════════════════
#                       FOOTER
# ═══════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888;'>LangGraph + Gemini + Tavily ile geliştirildi 🚀</p>",
    unsafe_allow_html=True
)