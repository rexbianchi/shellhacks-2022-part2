from io import StringIO
from os.path import exists
import pandas as pd
import crypt

class Vault:
    def __init__(self, encrypted_vault_location: str, vault_name, password):
        self.vault_location = encrypted_vault_location
        self.vault_name = vault_name
        self.password = password

    def get_accounts(self):
        if not exists(self.vault_location):
            crypt.new_account(self.vault_location, self.vault_name, self.password)
            return {}
        else:
            with open(self.vault_location) as file:
                encrypted_text = file.read()

            # csv_string = """myucf,rexb,08182003\nmybank,rexbianchi,ssfri48\nanotherbank,fdjhdkdd,dfjdhjdhjd"""

            csv_stringio = StringIO(crypt.decrypt(encrypted_text, self.vault_name, self.password))
            columns = ["Account", "Username", "Password"]
            df = pd.read_csv(csv_stringio, sep=",", header=None, names=columns, index_col="Account")

            dictionary = df.to_dict(orient="index")
            return dictionary

    def save_accounts(self, accounts: dict):
        df = pd.DataFrame.from_dict(accounts, orient="index")
        csv_stringio = StringIO()
        df.to_csv(csv_stringio, sep=",", header=False, index=False)
        encrypted_string = crypt.encrypt(csv_stringio.getvalue(), self.vault_name, self.password)
        with open(self.vault_location, "w") as file:
            file.write(encrypted_string)

if __name__ == "__main__":
    Vault("lol").save_accounts({'myucf': {'Username': 'rexb', 'Password': '08182003'}, 'mybank': {'Username': 'rexbianchi', 'Password': 'ssfri48'}, 'anotherbank': {'Username': 'fdjhdkdd', 'Password': 'dfjdhjdhjd'}}
)
