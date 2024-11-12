import requests

BASE_URL = "http://localhost:5000"

class ApiClient:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
    
    def _set_token(self, token):
        """Define o token JWT para autenticação."""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def login_employee(self, username, password):
        url = f"{BASE_URL}/login/employee"
        response = self.session.post(url, json={"username": username, "password": password})
        if response.status_code == 200:
            self._set_token(response.json()["access_token"])
        return response.json()

    def login_enterprise(self, company, password):
        url = f"{BASE_URL}/login/enterprise"
        response = self.session.post(url, json={"company": company, "password": password})
        if response.status_code == 200:
            self._set_token(response.json()["access_token"])
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
        response = self.session.put(url, json={"id_ponto": id_ponto, "hora_inicio": hora_inicio, "hora_final": hora_final})
        return response.json()

    def delete_point(self, id_ponto):
        url = f"{BASE_URL}/dashboard/enterprise"
        response = self.session.delete(url, json={"id_ponto": id_ponto})
        return response.json()


# Funções de teste para todas as rotas
if __name__ == "__main__":
    client = ApiClient()

    # Teste do login para funcionário
    print("Teste de login de funcionário:")
    response = client.login_employee("kaua", "123")
    print(response)

    # # Teste de login para empresa
    # print("\nTeste de login de empresa:")
    # response = client.login_enterprise("Creare", "123")
    # print(response)

    # Teste para registrar ponto de entrada
    print("\nTeste de registro de ponto de entrada:")
    response = client.record_entry_point()
    print(response)

    # # Teste para obter todos os pontos
    # print("\nTeste para obter todos os pontos:")
    # response = client.get_all_points()
    # print(response)

    # # Teste para atualizar ponto
    # print("\nTeste para atualizar ponto:")
    # response = client.update_point(1, "2024-01-01T08:00:00", "2024-01-01T17:00:00")
    # print(response)

    # # Teste para deletar ponto
    # print("\nTeste para deletar ponto:")
    # response = client.delete_point(1)
    # print(response)
