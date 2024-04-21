import requests


class BitrixClient:
    def __init__(self, domain: str, webhook: str):
        self.base_url = f"https://{domain}/rest/1/{webhook}"

    def get_contact(self, id: str) -> dict:
        response = requests.get(
            self.base_url + "/crm.contact.get",
            params={"ID": id},
        )
        return response.json()["result"]

    def update_contact(self, id: str, fields: dict) -> None:
        requests.post(
            self.base_url + "/crm.contact.update",
            data={
                "id": id,
                "fields": fields,
            },
        )
