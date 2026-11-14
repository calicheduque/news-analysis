import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise RuntimeError("ANTHROPIC_API_KEY not found in .env")

client = anthropic.Anthropic(api_key=api_key)

def probar_conexion():
    print("Conectando con Anthropic...")

    try:
        message = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=50,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": "Responde solo: API funcionando correctamente."
                }
            ]
        )

        print("\n✅ ¡Éxito!")

        for block in message.content:
            if block.type == "text":
                print(block.text)

    except anthropic.AuthenticationError:
        print("❌ API key inválida.")
    except anthropic.RateLimitError:
        print("❌ Rate limit o límite de uso.")
    except anthropic.APIConnectionError as e:
        print(f"❌ Error de conexión: {e}")
    except anthropic.APIStatusError as e:
        print(f"❌ API error {e.status_code}: {e.message}")
    except anthropic.APIError as e:
        print(f"❌ Error Anthropic: {e}")

if __name__ == "__main__":
    probar_conexion()
