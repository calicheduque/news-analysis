#poetry run python orchestrator.py
import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

# ---------------------------------------------------------
# 1. MOCK DE FLASHPOINT (Luego lo reemplazan por la API real)
# ---------------------------------------------------------
def get_flashpoint_sentiment(claim: str) -> str:
    """
    Simula la respuesta de Flashpoint.AI. 
    En el hackathon, esta función llamará al MCP o REST API.
    """
    print("⏳ Consultando segmentos en Flashpoint (Mock)...")
    
    # Datos simulados para el claim: "Rent prices are falling in NYC"
    mock_data = {
        "renters_harlem": {
            "source": "HUMANO",
            "n": 34,
            "quote": "My rent went up 12% this year. I don't care what the averages say."
        },
        "small_landlords_queens": {
            "source": "SINTÉTICO",
            "n": 20,
            "quote": "I haven't lowered rent, but I am giving one month free to fill vacancies."
        }
    }
    return json.dumps(mock_data, indent=2)

# ---------------------------------------------------------
# 2. PASO A: DESCOMPONER EL CLAIM (Anthropic)
# ---------------------------------------------------------
def decompose_claim(claim: str):
    print("🧠 Descomponiendo el claim con Claude...")
    prompt = f"""
    You are a rigorous fact-checking research assistant. 
    Break down the following public claim into 3 specific, verifiable sub-claims.
    
    Claim: "{claim}"
    
    Return ONLY a valid JSON list of strings. Example: ["Sub-claim 1", "Sub-claim 2", "Sub-claim 3"]
    """
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

# ---------------------------------------------------------
# 3. PASO B: SINTETIZAR EL ARTÍCULO (Anthropic)
# ---------------------------------------------------------
def synthesize_article(claim: str, sub_claims: str, flashpoint_data: str):
    print("✍️  Generando el artículo con etiquetas de procedencia...")
    
    prompt = f"""
    You are an investigative journalist. Write a short, punchy article based on the following data.
    
    CLAIM: {claim}
    
    SUB-CLAIMS TO VERIFY:
    {sub_claims}
    
    PRIVATE EXPERIENCE DATA (from Flashpoint.AI):
    {flashpoint_data}
    
    INSTRUCTIONS:
    1. Structure the article in Markdown with these sections:
       - # Claim: [The claim]
       - **Confidence: [0-100]%**
       - ## What public evidence shows (invent 1 plausible public stat)
       - ## What affected people say privately (use the Flashpoint data)
       - ## Where narrative and experience diverge
       - ## What we could NOT verify
    2. For every factual statement in the "private" section, prefix it with the source tag from the data: [HUMANO] or [SINTÉTICO].
    3. Be honest about what is missing.
    """
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

# ---------------------------------------------------------
# 4. PIPELINE PRINCIPAL
# ---------------------------------------------------------
if __name__ == "__main__":
    test_claim = "Rent prices are falling in NYC."
    
    print(f"🚀 Iniciando Agente para el claim: '{test_claim}'\n")
    
    # Paso 1: Descomponer
    sub_claims = decompose_claim(test_claim)
    print(f"✅ Sub-claims generados:\n{sub_claims}\n")
    
    # Paso 2: Consultar Flashpoint
    fp_data = get_flashpoint_sentiment(test_claim)
    print(f"✅ Datos de Flashpoint obtenidos.\n")
    
    # Paso 3: Sintetizar artículo
    article = synthesize_article(test_claim, sub_claims, fp_data)
    
    print("="*50)
    print("📰 ARTÍCULO FINAL:")
    print("="*50)
    print(article)
    
    # Guardar el resultado para que la UI (Persona B) lo pueda leer
    with open("demo_output.md", "w") as f:
        f.write(article)
    print("\n💾 Artículo guardado en demo_output.md")
