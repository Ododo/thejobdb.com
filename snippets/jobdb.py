import requests
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7

JOBDB_API = "https://thejobdb.com/api"
LOGIN_URL = JOBDB_API + "/login/"
JOBS_URL = JOBDB_API + "/jobs/"


def get_session(cakey_path, cacert_path, company_url):
    s = requests.Session()
    r = s.get(LOGIN_URL)
    challenge = r.json()["challenge"]

    assert r.status_code == 200

    with open(cakey_path, "rb") as ca_key, open(cacert_path, "rb") as ca_cert:
        key = serialization.load_pem_private_key(ca_key.read(), None)
        cert = x509.load_pem_x509_certificate(ca_cert.read())
        options = [pkcs7.PKCS7Options.DetachedSignature]
        data = pkcs7.PKCS7SignatureBuilder().set_data(
            challenge.encode()
        ).add_signer(cert, key, hashes.SHA256()
                     ).sign(serialization.Encoding.SMIME, options
                            )

    r = s.post(LOGIN_URL,
               data={"challenge_smime": data,
                     "company_url": company_url})

    assert r.status_code == 200

    return s
