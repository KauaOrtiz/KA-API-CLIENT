import requests

BASE_URL = "http://localhost:5000"  # Altere para o endereço da API se estiver em outro servidor

class ApiClient:
    def __init__(self):
        self.session = requests.Session()
    
    def login_employee(self, username, password):
        url = f"{BASE_URL}/login/employee"
        payload = {
            "username": username,
            "password": password
        }
        response = self.session.post(url, json=payload)
        return response.json()

    def create_employee(self, new_username, enterprise, position, new_password, confirm_password):
        url = f"{BASE_URL}/login/employee"
        payload = {
            "new_username": new_username,
            "enterprise": enterprise,
            "position": position,
            "new_password": new_password,
            "confirm_password": confirm_password
        }
        response = self.session.post(url, json=payload)
        return response.json()

    def login_enterprise(self, company, password):
        url = f"{BASE_URL}/login/enterprise"
        payload = {
            "company": company,
            "password": password
        }
        response = self.session.post(url, json=payload)
        return response.json()

    def create_enterprise(self, new_company, new_password, confirm_password):
        url = f"{BASE_URL}/login/enterprise"
        payload = {
            "new_company": new_company,
            "new_password": new_password,
            "confirm_password": confirm_password
        }
        response = self.session.post(url, json=payload)
        return response.json()

    def record_entry_point(self):
        url = f"{BASE_URL}/dashboard/employee"
        response = self.session.post(url)
        return response.json()

    def get_all_points(self):
        url = f"{BASE_URL}/dashboard/enterprise"
        response = self.session.get(url)
        return response.json()

    def update_point(self, id_ponto, hora_inicio, hora_final):
        url = f"{BASE_URL}/dashboard/enterprise"
        payload = {
            "id_ponto": id_ponto,
            "hora_inicio": hora_inicio,
            "hora_final": hora_final
        }
        response = self.session.put(url, json=payload)
        return response.json()

    def delete_point(self, id_ponto):
        url = f"{BASE_URL}/dashboard/enterprise"
        payload = {"id_ponto": id_ponto}
        response = self.session.delete(url, json=payload)
        return response.json()


# Exemplo de uso do cliente
if __name__ == "__main__":
    client = ApiClient()

    # Login como funcionário
    response = client.login_employee("user1", "password123")
    print("Login Employee:", response)

    # Criar um novo funcionário
    response = client.create_employee("new_user", "Enterprise1", "Manager", "password123", "password123")
    print("Create Employee:", response)

    # Login como empresa
    response = client.login_enterprise("company1", "password123")
    print("Login Enterprise:", response)

    # Criar uma nova empresa
    response = client.create_enterprise("new_company", "password123", "password123")
    print("Create Enterprise:", response)

    # Registrar ponto de entrada
    response = client.record_entry_point()
    print("Record Entry Point:", response)

    # Obter todos os pontos
    response = client.get_all_points()
    print("Get All Points:", response)

    # Atualizar um ponto
    response = client.update_point(id_ponto=1, hora_inicio="2024-11-10T08:00", hora_final="2024-11-10T17:00")
    print("Update Point:", response)

    # Deletar um ponto
    response = client.delete_point(id_ponto=1)
    print("Delete Point:", response)
