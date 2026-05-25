import anthropic
import os
import json
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT
from georisques import analyser_adresse

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyser_bien(adresse):
    """Analyse complète : données officielles + interprétation IA."""
    
    # Étape 1 : Récupérer les vraies données Géorisques
    print(f"\n📡 Récupération des données officielles...\n")
    donnees_officielles = analyser_adresse(adresse)
    
    if not donnees_officielles:
        print("❌ Impossible de récupérer les données pour cette adresse")
        return None
    
    # Étape 2 : Envoyer les données à l'IA pour interprétation
    print(f"\n🤖 Analyse IA en cours...\n")
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"""Voici les données officielles Géorisques pour le bien situé à : {adresse}

{json.dumps(donnees_officielles, indent=2, ensure_ascii=False)}

Produis un rapport complet selon ta structure habituelle en te basant uniquement sur ces données officielles."""
            }
        ]
    )
    
    rapport = message.content[0].text
    return rapport

if __name__ == "__main__":
    adresse = input("Entre une adresse à analyser : ")
    rapport = analyser_bien(adresse)
    
    if rapport:
        print(rapport)
        with open("outputs/rapport.txt", "w", encoding="utf-8") as f:
            f.write(f"Adresse : {adresse}\n\n")
            f.write(rapport)
        print("\n✅ Rapport sauvegardé dans outputs/rapport.txt")