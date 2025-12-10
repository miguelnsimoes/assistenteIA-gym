from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
import os
from google import genai
from pydantic import BaseModel

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    if GEMINI_API_KEY:
        client = genai.Client(api_key=GEMINI_API_KEY)
    else:
        print("api nao encontrada do gemini")
        client= None
except Exception as e:
    print("erro ao inicializar ia: {e}")
    client = None

app = FastAPI()


class PerfilUsuario(BaseModel):
    nome: str
    idade: int
    peso_kg: float
    altura_cm: int
    objetivo: str
    frequencia_semanal: int
    nivel_experiencia: str


@app.post("/gerar/plano")
def gerar_plano(perfil: PerfilUsuario):
    prompt = f"""
    Você é um Personal Trainer e Nutricionista IA altamente qualificado. Crie um Plano Completo (Dieta e Treino)
    para o usuário. O formato da saída deve ser claro e profissional, utilizando formatação Markdown (títulos, negrito e listas).

    ### Dados do Usuário:
    - Nome: {perfil.nome}
    - Idade: {perfil.idade} anos
    - Peso: {perfil.peso_kg} kg
    - Altura: {perfil.altura_cm} cm
    - Objetivo: {perfil.objetivo}
    - Nível de Experiência: {perfil.nivel_experiencia}
    - Treino Semanal: {perfil.frequencia_semanal} dias

    ### Instruções do Plano:
    1. Crie uma seção de Treino para {perfil.frequencia_semanal} dias por semana, detalhando exercícios e séries.
    2. Crie uma seção de Dieta, com exemplos de refeições (Café, Almoço, Jantar) para o objetivo de {perfil.objetivo}.
    """
    try:
        resposta = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )

        return{
            "status": "plano gerado com sucesso",
            "plano_markdown": resposta.text
        }
    
    except Exception as e:
        return{
            "error": f"falha ao gerar plano com IA: {e}"
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)