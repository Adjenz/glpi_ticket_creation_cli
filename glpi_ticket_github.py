import requests
import readline  # Pour la complétion automatique (TAB)
import json  # Pour un meilleur affichage des réponses JSON

# Informations de connexion
URL = "Your GLPI URL"
USER_TOKEN = "Your user token"
APP_TOKEN = "Your app token"

def get_technicians(session_token, search_term):
    headers = {
        'Session-Token': session_token,
        'App-Token': APP_TOKEN
    }
    
    try:
        # Recherche des techniciens
        params = {
            'is_assign': True,  # Pour filtrer les techniciens
            'range': '0-1000'
        }
        
        response = requests.get(f"{URL}/User", headers=headers, params=params)
        
        if response.status_code in [200, 206]:
            users = response.json()
            
            # Filtrer les techniciens qui correspondent au terme de recherche
            matching_users = []
            search_term_lower = search_term.lower()
            
            for user in users:
                name = str(user.get('name', '')).lower()
                realname = str(user.get('realname', '')).lower()
                firstname = str(user.get('firstname', '')).lower()
                
                if (search_term_lower in name or 
                    search_term_lower in realname or 
                    search_term_lower in firstname):
                    matching_users.append(user)
            
            if matching_users:
                print("\nTechniciens correspondants trouvés :")
                for user in matching_users:
                    user_info = []
                    if user.get('id'):
                        user_info.append(f"ID : {user['id']}")
                    if user.get('name'):
                        user_info.append(f"Nom : {user['name']}")
                    if user.get('firstname'):
                        user_info.append(f"Prénom : {user['firstname']}")
                    if user.get('realname'):
                        user_info.append(f"Nom complet : {user['realname']}")
                    
                    print(" - ".join(user_info))
                return matching_users
            else:
                print("Aucun technicien ne correspond à votre recherche")
                return []
        else:
            print(f"Erreur lors de la recherche des techniciens. Code : {response.status_code}")
            if hasattr(response, 'text'):
                print(f"Détails : {response.text}")
            return []
            
    except Exception as e:
        print(f"Exception lors de la recherche des techniciens : {str(e)}")
        return []

def init_session():
    headers = {
        'Authorization': f'user_token {USER_TOKEN}',
        'App-Token': APP_TOKEN
    }
    response = requests.post(f"{URL}/initSession", headers=headers)
    if response.status_code == 200:
        session_token = response.json().get('session_token')
        print("Session initialisée avec succès.")
        return session_token
    else:
        print("Erreur d'initialisation de la session :", response.text)
        return None

def get_categories(session_token, display_all=False):
    headers = {
        'Session-Token': session_token,
        'App-Token': APP_TOKEN
    }
    response = requests.get(f"{URL}/ITILCategory", headers=headers)
    if response.status_code == 200:
        categories = response.json()
        if display_all:
            print("\nCatégories disponibles :")
            for cat in categories:
                print(f"ID : {cat['id']} - Nom : {cat['name']}")
        return categories
    else:
        print("Erreur lors de la récupération des catégories :", response.text)
        return []

def get_users(session_token, search_term):
    headers = {
        'Session-Token': session_token,
        'App-Token': APP_TOKEN
    }
    
    try:
        # Utilisation de l'endpoint pour rechercher des utilisateurs/demandeurs
        params = {
            'is_requester': True,  # Pour filtrer les demandeurs
            'range': '0-1000'      # Pour obtenir plus de résultats
        }
        
        response = requests.get(f"{URL}/User", headers=headers, params=params)
        
        if response.status_code in [200, 206]:
            users = response.json()
            
            # Filtrer les utilisateurs qui correspondent au terme de recherche
            matching_users = []
            search_term_lower = search_term.lower()
            
            for user in users:
                # Récupérer les champs avec des valeurs par défaut vides si non présents
                name = str(user.get('name', '')).lower()
                realname = str(user.get('realname', '')).lower()
                firstname = str(user.get('firstname', '')).lower()
                
                # Vérifier si le terme de recherche est dans l'un des champs
                if (search_term_lower in name or 
                    search_term_lower in realname or 
                    search_term_lower in firstname):
                    matching_users.append(user)
            
            if matching_users:
                print("\nUtilisateurs correspondants trouvés :")
                for user in matching_users:
                    user_info = []
                    if user.get('id'):
                        user_info.append(f"ID : {user['id']}")
                    if user.get('name'):
                        user_info.append(f"Nom : {user['name']}")
                    if user.get('firstname'):
                        user_info.append(f"Prénom : {user['firstname']}")
                    if user.get('realname'):
                        user_info.append(f"Nom complet : {user['realname']}")
                    
                    print(" - ".join(user_info))
                return matching_users
            else:
                print("Aucun utilisateur ne correspond à votre recherche")
                return []
        else:
            print(f"Erreur lors de la recherche des utilisateurs. Code : {response.status_code}")
            if hasattr(response, 'text'):
                print(f"Détails : {response.text}")
            return []
            
    except Exception as e:
        print(f"Exception lors de la recherche des utilisateurs : {str(e)}")
        return []

def get_category_name(session_token, category_id):
    """Récupère le nom de la catégorie à partir de son ID"""
    headers = {
        'Session-Token': session_token,
        'App-Token': APP_TOKEN
    }
    
    response = requests.get(f"{URL}/ITILCategory/{category_id}", headers=headers)
    if response.status_code == 200:
        category_data = response.json()
        if category_data:
            return category_data.get('name', f"Catégorie {category_id}")
    return f"Catégorie {category_id}"  # Fallback si non trouvé

def get_user_name(session_token, user_id):
    """Récupère le nom de l'utilisateur à partir de son ID"""
    headers = {
        'Session-Token': session_token,
        'App-Token': APP_TOKEN
    }
    
    response = requests.get(f"{URL}/User/{user_id}", headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        if user_data:
            return user_data.get('name', f"Utilisateur {user_id}")
    return f"Utilisateur {user_id}"  # Fallback si non trouvé

def search_categories(categories, search_term):
    """Recherche dans les catégories selon un terme."""
    search_term = search_term.lower()
    matching_categories = []
    for cat in categories:
        if search_term in cat['name'].lower():
            matching_categories.append(cat)
    return matching_categories

def display_categories(categories):
    """Affiche les catégories de manière formatée."""
    print("\nCatégories disponibles :")
    for cat in categories:
        print(f"ID : {cat['id']} - {cat['name']}")

def select_category(session_token):
    """Interface interactive pour la sélection de catégorie."""
    categories = get_categories(session_token)
    if not categories:
        print("❌ Impossible de récupérer les catégories.")
        return None

    while True:
        print("\n🔍 Pour la catégorie, vous pouvez :")
        print("  1. Voir toutes les catégories")
        print("  2. Rechercher une catégorie")
        print("  3. Entrer directement un ID")
        choice = input("\nVotre choix (1-3) : ")

        if choice == "1":
            display_categories(categories)
        elif choice == "2":
            search_term = input("Entrez le terme de recherche : ")
            matching_cats = search_categories(categories, search_term)
            if matching_cats:
                display_categories(matching_cats)
            else:
                print("❌ Aucune catégorie trouvée avec ce terme.")
        elif choice == "3" or choice.isdigit():
            cat_id = choice if choice.isdigit() else input("Entrez l'ID de la catégorie : ")
            if not cat_id.isdigit():
                print("❌ L'ID doit être un nombre.")
                continue
            if any(cat['id'] == int(cat_id) for cat in categories):
                return cat_id
            print("❌ ID de catégorie invalide.")

def validate_email(email):
    """Valide le format de l'email."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None if email else True

def validate_phone(phone):
    """Valide le format du numéro de téléphone."""
    import re
    if not phone:  # Accepte un numéro vide
        return True
    # Accepte les formats: 0123456789, 01 23 45 67 89, +33123456789
    pattern = r'^(\+33|0)[1-9]([-. ]?[0-9]{2}){4}$'
    return bool(re.match(pattern, phone))

def confirm_ticket_creation(ticket_data, session_token):
    """Affiche un résumé du ticket et demande confirmation."""
    print("\n📋 Résumé du ticket :")
    print("=" * 50)
    print(f"Titre : {ticket_data['title']}")
    print(f"\nDescription :")
    print(ticket_data['description_text'])
    
    # Récupérer les noms au lieu des IDs
    category_name = get_category_name(session_token, ticket_data['category_id'])
    requester_name = get_user_name(session_token, ticket_data['requester_id'])
    assignee_name = get_user_name(session_token, ticket_data['assignee_id'])
    
    print(f"\nCatégorie : {category_name}")
    print(f"Demandeur : {requester_name}")
    print(f"Technicien assigné : {assignee_name}")
    print("=" * 50)
    
    while True:
        confirm = input("\nVoulez-vous créer ce ticket ? (o/n) : ").lower()
        if confirm in ['o', 'n']:
            return confirm == 'o'
        print("❌ Veuillez répondre par 'o' ou 'n'")

def collect_ticket_information(session_token):
    try:
        # 1. Titre du ticket
        title = input("\nEntrez le titre du ticket : ")
        if not title.strip():
            print("❌ Le titre ne peut pas être vide.")
            return None

        # 2. Description interactive
        caller_name = input("Nom de l'appelant : ")
        
        while True:
            phone_number = input("Numéro de téléphone : ")
            if validate_phone(phone_number):
                break
            print("❌ Format de numéro invalide. Utilisez un format valide (ex: 0123456789 ou +33123456789)")
        
        while True:
            email = input("E-mail : ")
            if validate_email(email):
                break
            print("❌ Format d'email invalide.")
            
        copier_serial = input("Est-ce que ça concerne un copieur ? (laisser vide si non, sinon entrez le numéro de série) : ")
        incident_description = input("Description de l'incident : ")
        if not incident_description.strip():
            print("❌ La description ne peut pas être vide.")
            return None

        # Construction de la description
        description_text = f"""
📞 Informations de contact :
------------------------
👤 Nom de l'appelant    : {caller_name}
📱 Numéro de téléphone : {phone_number}
📧 E-mail              : {email}
{"🖨️ N° de série copieur : " + copier_serial if copier_serial else ""}

📝 Description de l'incident :
------------------------
{incident_description}
"""

        description_html = f"""
<div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px;'>
    <h4 style='color: #0056b3; margin-top: 0;'>📞 Informations de contact</h4>
    <table style='width: 100%; border-collapse: collapse;'>
        <tr>
            <td style='padding: 5px; width: 180px;'><strong>👤 Nom de l'appelant :</strong></td>
            <td style='padding: 5px;'>{caller_name}</td>
        </tr>
        <tr>
            <td style='padding: 5px;'><strong>📱 Numéro de téléphone :</strong></td>
            <td style='padding: 5px;'>{phone_number}</td>
        </tr>
        <tr>
            <td style='padding: 5px;'><strong>📧 E-mail :</strong></td>
            <td style='padding: 5px;'>{email}</td>
        </tr>
        {"<tr><td style='padding: 5px;'><strong>🖨️ N° de série copieur :</strong></td><td style='padding: 5px;'>" + copier_serial + "</td></tr>" if copier_serial else ""}
    </table>

    <h4 style='color: #0056b3; margin-top: 15px;'>📝 Description de l'incident</h4>
    <div style='background-color: white; padding: 10px; border-radius: 3px; border: 1px solid #dee2e6;'>
        {incident_description}
    </div>
</div>
"""

        # 3. Catégorie
        print("\n⏳ Sélection de la catégorie...")
        category_id = select_category(session_token)
        if not category_id:
            print("❌ Impossible de sélectionner une catégorie. Veuillez réessayer.")
            return None

        # 4. Recherche et sélection du demandeur
        while True:
            search_term = input("\nEntrez le nom du demandeur (ou partie du nom) : ")
            if not search_term:
                print("❌ La recherche ne peut pas être vide.")
                continue
            
            print("⏳ Recherche des utilisateurs...")
            users = get_users(session_token, search_term)
            if users:
                user_id = input("\nEntrez l'ID du demandeur choisi : ")
                if user_id.isdigit() and any(user['id'] == int(user_id) for user in users):
                    requester_id = int(user_id)
                    
                    # Récupérer et définir l'entité de l'utilisateur
                    entity_info = get_user_entity(session_token, user_id)
                    if entity_info:
                        entities_id = entity_info['id']
                        print(f"\nEntité du demandeur : {entity_info['completename']}")
                    else:
                        entities_id = None
                    break
                else:
                    print("ID utilisateur invalide.")
            else:
                retry = input("Voulez-vous effectuer une nouvelle recherche ? (O/n) : ")
                if retry.lower() == 'n':
                    return None

        # 5. Recherche et sélection du technicien
        while True:
            print("\n🔍 Pour le technicien, vous pouvez :")
            print("  - Entrer directement un ID")
            print("  - Entrer un nom pour rechercher")
            tech_input = input("Votre choix : ")

            if tech_input.isdigit():
                assignee_id = tech_input
                print("⏳ Vérification de l'ID du technicien...")
                headers = {
                    'Session-Token': session_token,
                    'App-Token': APP_TOKEN
                }
                response = requests.get(f"{URL}/User/{tech_input}", headers=headers)
                if response.status_code == 200:
                    tech = response.json()
                    # Vérifier si l'utilisateur est dans le groupe des techniciens
                    params = {
                        'is_assign': True,
                        'range': '0-1000'
                    }
                    tech_response = requests.get(f"{URL}/User", headers=headers, params=params)
                    if tech_response.status_code == 200:
                        technicians = tech_response.json()
                        if any(t['id'] == int(tech_input) for t in technicians):
                            break
                        else:
                            print("❌ L'ID fourni n'est pas celui d'un technicien.")
                    else:
                        print("❌ Erreur lors de la vérification du statut technicien.")
                else:
                    print("❌ ID de technicien invalide.")
            else:
                print("⏳ Recherche des techniciens...")
                technicians = get_technicians(session_token, tech_input)
                if technicians:
                    tech_id = input("\nEntrez l'ID du technicien choisi (ou Entrée pour chercher à nouveau) : ")
                    if tech_id:
                        if not tech_id.isdigit():
                            print("❌ L'ID doit être un nombre.")
                            continue
                        if any(tech['id'] == int(tech_id) for tech in technicians):
                            assignee_id = tech_id
                            break
                        else:
                            print("❌ ID invalide parmi les résultats.")
                else:
                    print("❌ Aucun technicien trouvé avec ce nom.")

        ticket_data = {
            "title": title,
            "description": description_html,
            "description_text": description_text,
            "category_id": category_id,
            "requester_id": requester_id,
            "entities_id": entities_id,
            "assignee_id": assignee_id
        }

        # Confirmation avant création
        if not confirm_ticket_creation(ticket_data, session_token):
            print("\n❌ Création du ticket annulée.")
            return None

        return ticket_data

    except KeyboardInterrupt:
        print("\n\n⚠️ Création du ticket annulée.")
        return None
    except Exception as e:
        print(f"\n❌ Une erreur est survenue : {str(e)}")
        return None

def get_user_entity(session_token, user_id):
    """Récupère l'entité d'un utilisateur à partir de son ID"""
    headers = {
        'Session-Token': session_token,
        'App-Token': APP_TOKEN
    }
    
    try:
        # Récupérer les profils de l'utilisateur
        profile_response = requests.get(f"{URL}/User/{user_id}/Profile_User?expand_dropdowns=true", headers=headers)
        
        if profile_response.status_code == 200:
            profiles = profile_response.json()
            
            if profiles:
                # Récupérer l'entité de l'utilisateur
                for profile in profiles:
                    entity_link = next((link['href'] for link in profile.get('links', []) if link['rel'] == 'Entity'), None)
                    if entity_link:
                        # Récupérer les détails de l'entité de l'utilisateur
                        entity_response = requests.get(entity_link, headers=headers)
                        if entity_response.status_code == 200:
                            entity_data = entity_response.json()
                            # Récupérer l'entité parente (CLIENTS_SOUS_CONTRAT)
                            parent_id = entity_data.get('entities_id')
                            if parent_id:
                                parent_response = requests.get(f"{URL}/Entity/{parent_id}?expand_dropdowns=true", headers=headers)
                                if parent_response.status_code == 200:
                                    parent_data = parent_response.json()
                                    return {
                                        'id': parent_id,
                                        'name': parent_data.get('name', 'Entité inconnue'),
                                        'completename': parent_data.get('completename', 'Entité inconnue')
                                    }
                            
        print("\nAucune entité parente trouvée pour l'utilisateur.")
        return None
    except Exception as e:
        print(f"\nErreur lors de la récupération de l'entité : {str(e)}")
        return None

def create_ticket(session_token, ticket_data):
    headers = {
        'Session-Token': session_token,
        'App-Token': APP_TOKEN,
        'Content-Type': 'application/json'
    }

    # Extraction des données du ticket
    title = ticket_data["title"]
    description = ticket_data["description"]
    category_id = ticket_data["category_id"]
    requester_id = ticket_data["requester_id"]
    entities_id = ticket_data.get("entities_id", None)
    assignee_id = ticket_data["assignee_id"]

    payload = {
        "input": {
            "name": title,
            "content": description,
            "itilcategories_id": category_id,
            "_users_id_requester": [requester_id],
            "entities_id": entities_id,
            "_users_id_assign": [assignee_id],
            "status": 1,
            "type": 1,
            "urgency": 3,
            "impact": 3
        }
    }

    response = requests.post(f"{URL}/Ticket", headers=headers, json=payload)
    
    if response.status_code == 201:
        ticket_id = response.json()["id"]
        print(f"\n✅ Ticket créé avec succès ! ID : {ticket_id}")
        
        # Proposer de résoudre le ticket
        resolve = input("\nVoulez-vous résoudre ce ticket maintenant ? (o/N) : ")
        if resolve.lower() == 'o':
            resolve_ticket(session_token, ticket_id)
        
        return True
    else:
        print("\n❌ Erreur lors de la création du ticket :")
        if hasattr(response, 'text'):
            print(response.text)
        return None

def resolve_ticket(session_token, ticket_id):
    """Résout un ticket en demandant la solution et propose l'approbation"""
    headers = {
        'Session-Token': session_token,
        'App-Token': APP_TOKEN,
        'Content-Type': 'application/json'
    }

    try:
        print("\n📝 Entrez la solution pour résoudre le ticket :")
        print("(Appuyez sur Entrée deux fois pour terminer)")
        
        lines = []
        while True:
            line = input()
            if line:
                lines.append(line)
            else:
                break
        
        solution = "\n".join(lines)
        
        if not solution.strip():
            print("❌ Aucune solution fournie. Le ticket reste ouvert.")
            return False

        # 1. Créer le suivi avec la solution
        followup_payload = {
            "input": {
                "itemtype": "Ticket",
                "items_id": ticket_id,
                "content": solution,
                "is_private": 0
            }
        }
        
        followup_response = requests.post(
            f"{URL}/ITILFollowup",
            headers=headers,
            json=followup_payload
        )
        
        if followup_response.status_code != 201:
            print(f"❌ Erreur lors de l'ajout de la solution : {followup_response.text}")
            return False

        # 2. Ajouter la solution
        solution_payload = {
            "input": {
                "itemtype": "Ticket",
                "items_id": ticket_id,
                "content": solution
            }
        }
        
        solution_response = requests.post(
            f"{URL}/ITILSolution",
            headers=headers,
            json=solution_payload
        )
        
        if solution_response.status_code != 201:
            print(f"❌ Erreur lors de l'ajout de la solution : {solution_response.text}")
            return False

        # 3. Mettre le ticket en résolu
        ticket_payload = {
            "input": {
                "id": ticket_id,
                "status": 5  # 5 = Résolu
            }
        }
        
        ticket_response = requests.put(
            f"{URL}/Ticket/{ticket_id}",
            headers=headers,
            json=ticket_payload
        )
        
        if ticket_response.status_code != 200:
            print(f"❌ Erreur lors de la mise en résolu du ticket : {ticket_response.text}")
            return False

        print("✅ Solution ajoutée et ticket mis en résolu !")

        # 4. Proposer l'approbation
        approve = input("\nVoulez-vous approuver la solution et clore le ticket ? (o/N) : ")
        if approve.lower() == 'o':
            solution_id = solution_response.json()["id"]

            # Approuver la solution
            approve_payload = {
                "input": {
                    "id": solution_id,
                    "status": 3  # 3 = Approuvé
                }
            }
            
            approve_response = requests.put(
                f"{URL}/ITILSolution/{solution_id}",
                headers=headers,
                json=approve_payload
            )
            
            if approve_response.status_code != 200:
                print(f"❌ Erreur lors de l'approbation de la solution : {approve_response.text}")
                return False

            # Mettre le ticket en clos
            close_payload = {
                "input": {
                    "id": ticket_id,
                    "status": 6  # 6 = Clos
                }
            }
            
            close_response = requests.put(
                f"{URL}/Ticket/{ticket_id}",
                headers=headers,
                json=close_payload
            )
            
            if close_response.status_code != 200:
                print(f"❌ Erreur lors de la clôture du ticket : {close_response.text}")
                return False

            print("✅ Solution approuvée et ticket clos avec succès !")
        
        return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la résolution du ticket : {str(e)}")
        return False

def close_session(session_token):
    headers = {
        'Session-Token': session_token,
        'App-Token': APP_TOKEN
    }
    response = requests.post(f"{URL}/killSession", headers=headers)
    if response.status_code == 200:
        print("Session fermée avec succès.")
    else:
        print("Erreur lors de la fermeture de la session :", response.text)

if __name__ == "__main__":
    session_token = init_session()
    if session_token:
        ticket_data = collect_ticket_information(session_token)
        if ticket_data and ticket_data["requester_id"] and ticket_data["assignee_id"]:
            create_ticket(session_token, ticket_data)
        else:
            print("Création du ticket annulée car aucun demandeur ou technicien n'a été sélectionné.")
        close_session(session_token)
