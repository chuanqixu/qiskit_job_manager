import os, json
from qiskit import IBMQ

def load_credential(credential_path = None):
    if not credential_path:
        credential_path = os.path.join(os.path.dirname(__file__), "provider_credential.json")
    with open(credential_path, "r") as f:
        credential = json.load(f)
    return credential

def load_provider(credential_path = None):
    if not credential_path:
        credential_path = os.path.join(os.path.dirname(__file__), "provider_credential.json")
    credential = load_credential(credential_path)
    
    IBMQ.load_account()
    return IBMQ.get_provider(hub = credential["hub"], group = credential["group"], project = credential["project"])
