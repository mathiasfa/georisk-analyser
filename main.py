import anthropic
import os
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT

# Charger la clé API depuis .env
load_dotenv()

# Initialiser le client Anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyser_bien(adresse):
    """Analyse les risques environnementaux d'un bien immobilier."""
    
    print(f"\n🔍 Analyse en cours pour : {adresse}\n")
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Analyse les risques environnementaux pour ce bien immobilier : {adresse}. Produis un rapport complet selon ta structure habituelle."
            }
        ]
    )
    
    rapport = message.content[0].text
    return rapport

# Test
if __name__ == "__main__":
    adresse = input("Entre une adresse à analyser : ")
    rapport = analyser_bien(adresse)
    print(rapport)
    
    # Sauvegarder le rapport
    with open(f"outputs/rapport.txt", "w", encoding="utf-8") as f:
        f.write(rapport)
    print("\n✅ Rapport sauvegardé dans outputs/rapport.txt")
    