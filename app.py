import streamlit as st
from main import create_graph, AgentState
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="Araştırma Asistanı", page_icon="🔍")

st.title("🔍 Araştırma Asistanı")
st.markdown("*LangGraph ile güçlendirilmiş AI araştırma aracı*")

query = st.text_input("📌 Araştırmak istediğiniz konuyu girin:", placeholder="Örn: Docker nedir?")

if st.button("🚀 Araştır", type="primary", use_container_width=True):
    if query:
        with st.spinner("🔄 Araştırılıyor..."):
            app = create_graph()
            
            result = app.invoke({
                "messages": [HumanMessage(content=query)],
                "query": query,
                "research_data": "",
                "summary": "",
                "revision_count": 0
            })
        
        st.success("✅ Araştırma tamamlandı!")
        st.subheader("📄 Özet")
        st.markdown(result["summary"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Revizyon Sayısı", result["revision_count"])
        with col2:
            st.metric("Özet Uzunluğu", f"{len(result['summary'])} karakter")
    else:
        st.warning("⚠️ Lütfen bir konu girin!")