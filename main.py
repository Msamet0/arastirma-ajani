from typing import TypedDict, Annotated, Sequence, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import operator
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END, START

load_dotenv()

#1.Durun State Tanımlama
class AgentState(TypedDict):
    # Annotated ve operator.add sayesinde yeni mesajlar listeye silinmeden eklenir.
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str              # Kullanıcıdan alınan sorgu
    research_data: str      # Araştırma sonuçları
    summary: str            # Yazılan özet
    revision_count: int     # Kaç kez revize edildi (sonsuz döngü önleme)
#---------------------------------------------------------------------------#
# 2.Pydantic Modeller
class Source(BaseModel):
    url: str = Field(description="URL of the source")

class AgentResponse(BaseModel):
    answer: str = Field(description="The agent's answer in MARKDOWN format")
    sources: List[Source] = Field(default_factory=list, description="List of sources used")
#----------------------------------------------------------------------------
# 3. DÜĞÜM FONKSİYONLARI (NODES)
def researcher_node(state: AgentState) -> dict:
    print("🔍 Araştırmacı çalışıyor...")
    tavily = TavilySearch(max_results=5)
    query = state["query"]
    results = tavily.invoke({"query": query})
    return {"research_data": str(results)}

def writer_node(state: AgentState) -> dict:
    print("✍️ Yazar çalışıyor...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    düzeltme_sayacı=state.get("revision_count", 0)
    önceki_özet=state.get("summary", "")

    if düzeltme_sayacı > 0:
        prompt = f"""
    You are an expert researcher. 
    Subject: {state['query']}
    Research Data: {state['research_data']}

    Please prepare a summary in TURKISH using MARKDOWN format.
    Rules:
    1. Use # for main title and ## for sections.
    2. Use **bold** for technical terms.
    3. Use bullet points for lists.
    4. Keep technical depth but simplify the language.
    5. Output must be at least 500 characters.

    RULES for Links:
    - At the end of the summary, create a '### Kaynakça' section.
    - For each source, use this format: [Site Adı - Sayfa Başlığı](URL)
    - Example: [T.C. Cumhurbaşkanlığı](https://www.tccb.gov.tr)
    
    """
    else:
        prompt = f"""
    You are an expert researcher. 
    Subject: {state['query']}
    Research Data: {state['research_data']}

    Please prepare a summary in TURKISH using MARKDOWN format.
    Rules:
    1. Use # for main title and ## for sections.
    2. Use **bold** for technical terms.
    3. Use bullet points for lists.
    4. Keep technical depth but simplify the language.
    5. Output must be at least 500 characters.

    RULES for Links:
    - At the end of the summary, create a '### Kaynakça' section.
    - For each source, use this format: [Site Adı - Sayfa Başlığı](URL)
    - Example: [T.C. Cumhurbaşkanlığı](https://www.tccb.gov.tr)
    
    """   

    response = llm.invoke([HumanMessage(content=prompt)])
    return {
        "summary": response.content,
        "revision_count": düzeltme_sayacı + 1,
        "messages": [response]
    }

# 4. NODE 3: EDİTÖR (KARAR FONKSİYONU)
def editor_decision(state: AgentState) -> str:
    """Özetin kalitesini kontrol eder ve bir sonraki adıma karar verir"""
    print("📝 Editör kontrol ediyor...")
    summary = state.get("summary", "")
    revision_count = state.get("revision_count", 0)
    
    # Sonsuz döngü önleme: Maximum 3 revizyon
    if revision_count >= 3:
        print("⚠️ Maximum revizyon sayısına ulaşıldı. Bitiriliyor...")
        return "finish"
    
    # Özet uzunluk kontrolü (500 karakterden az ise kısa)
    if len(summary) < 500:
        print(f" Özet çok kısa ({len(summary)} karakter). Yazara geri gönderiliyor...")
        return "revise"
    
    print(f" Özet yeterli ({len(summary)} karakter). Tamamlandı!")
    return "finish"

# 5. GRAF OLUŞTURMA
def create_graph():
    graph = StateGraph(AgentState)
    
    # Düğümleri ekle
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)
    
    # Kenarları ekle
    graph.add_edge(START, "researcher")           # Başla -> Araştırmacı
    graph.add_edge("researcher", "writer")        # Araştırmacı -> Yazar
    
    # Koşullu kenar: Editör kararı
    graph.add_conditional_edges(
        "writer",           # Kaynak düğüm (Yazar)
        editor_decision,    # Karar fonksiyonu
        {
            "revise": "writer",  # Özet kısa -> Yazara geri dön (DÖNGÜ)
            "finish": END        # Özet iyi -> Bitir
        }
    )
    
    return graph.compile()

# 6. ANA FONKSİYON
def main():
    print("=" * 50)
    print("🤖 Araştırma Asistanı")
    print("=" * 50)
    
    app = create_graph()
    
    user_input = input("\n📌 Araştırmak istediğiniz konuyu giriniz: ")
    
    result = app.invoke({
        "messages": [HumanMessage(content=user_input)],
        "query": user_input,
        "research_data": "",
        "summary": "",
        "revision_count": 0
    })
    
    
    print(" SONUÇ:")
   
    print(result["summary"])
  
    print(f" Toplam revizyon sayısı: {result['revision_count']}")

if __name__ == "__main__":
    main()
