import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 256,
}

system_instruction = """Você é um assistente de jogos online e afiliado da 1win.
Regras: Responda de forma simples, curta e clara (máximo 5 a 8 linhas).
Foco em explicações. Não prometa lucro garantido ou ganhos.
Não incentive apostas irresponsáveis. Mantenha tom neutro e informativo.
Sem hype exagerado."""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config,
    system_instruction=system_instruction
)

def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "No momento estou processando muitos dados. Pode tentar perguntar de novo?"