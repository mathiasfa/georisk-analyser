import requests

def get_adresse_coords(adresse):
    """Convertit une adresse en coordonnées GPS via l'API du gouvernement."""
    url = "https://api-adresse.data.gouv.fr/search/"
    params = {"q": adresse, "limit": 1}
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if not data["features"]:
        return None, None
    
    coords = data["features"][0]["geometry"]["coordinates"]
    lon, lat = coords[0], coords[1]
    print(f"📍 Coordonnées trouvées : lat={lat}, lon={lon}")
    return lat, lon

def get_risques_georisques(lat, lon):
    """Récupère les risques officiels depuis l'API Géorisques."""
    url = "https://georisques.gouv.fr/api/v1/resultats_rapport_risque"
    params = {
        "latlon": f"{lon},{lat}",
        "rayon": 1000
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Erreur API Géorisques : {response.status_code}")
        return None
        
    return response.json()

def analyser_adresse(adresse):
    """Pipeline complet : adresse → coordonnées → données Géorisques."""
    print(f"🔍 Récupération des données officielles pour : {adresse}")
    
    lat, lon = get_adresse_coords(adresse)
    if not lat:
        print("❌ Adresse non trouvée")
        return None
    
    risques = get_risques_georisques(lat, lon)
    if not risques:
        print("❌ Données Géorisques non disponibles")
        return None
    
    print("✅ Données officielles récupérées")
    return risques

# Test
if __name__ == "__main__":
    adresse = input("Entre une adresse : ")
    data = analyser_adresse(adresse)
    if data:
        import json
        print(json.dumps(data, indent=2, ensure_ascii=False))
        