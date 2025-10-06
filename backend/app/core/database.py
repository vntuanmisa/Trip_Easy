from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os

# Create SSL certificate file
ca_cert_content = """-----BEGIN CERTIFICATE-----
MIIEUDCCArigAwIBAgIUEZaAWNO0/ni5NsqJdJCI2lY0n/IwDQYJKoZIhvcNAQEM
BQAwQDE+MDwGA1UEAww1ZmMzY2MxYTQtY2JhYi00MTgzLTg4ZWItMjc3MGMyYzkw
Yjg3IEdFTiAxIFByb2plY3QgQ0EwHhcNMjUxMDAyMDQ0OTA0WhcNMzUwOTMwMDQ0
OTA0WjBAMT4wPAYDVQQDDDVmYzNjYzFhNC1jYmFiLTQxODMtODhlYi0yNzcwYzJj
OTBiODcgR0VOIDEgUHJvamVjdCBDQTCCAaIwDQYJKoZIhvcNAQEBBQADggGPADCC
AYoCggGBAN5VU5CiO/pkfP+Lrnw7DSo8qjcmielyKB9BTyPnejfAw1PwPHO2INlu
7GhzVcoyuNiX+D/BsWwx/HWem+0i3xGrC5c+N2lZTJxXg/tTw9SxFLDfr6FwQQ4x
ps1M3tmityKCKc+eoSouGc+JMp8xjMOU9KBDeyca4e/3RL2i8V2AphbYT6w7z0Uk
/qkCNVTfM0phyyEggku+HIgSGzd+H3sTZ3LOayeY0MWEYxbOwKjGkiSlMkbzFawP
IeNxwpom+e3Ei1lGD/Bt6/ntJnc9tV3ksHjobi8PKGXpTD4ob1byIsCMobGdvjfe
yxLo3Jp+awkEuvrAlrn3SBNRDEqtuHt7l8siY48Mv6c8d7vvy3qKzQCpQit2P+u8
xvpLL7idO6Btb7eCyi7OLSst0q3L/BHTDrEjqT7AAmoYuxUDYrchKZ67DS3vE8Uu
qzPGoMygGYjq6gGDjB/dV1RKAuSaWpS8CwqmpG/mtNFFZMBBvKGJKkh2q5r2wEHZ
aWi28WGhHQIDAQABo0IwQDAdBgNVHQ4EFgQUZFR7awp04U+x3aV1+qAPz9We3bEw
EgYDVR0TAQH/BAgwBgEB/wIBADALBgNVHQ8EBAMCAQYwDQYJKoZIhvcNAQEMBQAD
ggGBAA4sHAJgvYOdUdhHtU9wygkkx/2zVD/DN3ZvViNzzpeVB2DckDaE/8a6HPGb
kCR0OLgxtzAUnYFGchsPuy4S3GTbxrJW3GeN2mmoebAvV8XvRe1AAk3cPLybJqz5
kArzcOtYj6addhr8wBA0pDYOFoll149+mOxTZlRNsxQwA8xkhM3YzY5UjOFr9Yl0
l5Gwyx80tfAtvrHRGPmfubHscZQT3jyH5nkmZrokQEwV/MX2CaeZ0/PmiqcLrI87
rTIntMQQE9aF1LEKiOPBU9PhCXfp0dfRtX5LeV6E1HF40wxloHd+UzkskPULfY7K
t9I1+SV15lgSs2/4cP3AdB3Q+UN5WdQO/DsBsrlkbC98IIJOKIaU8QTDtNCdPOxV
446r0qGm5WVdtbDhzUR0iIma5FAkgwlfCiAF8/ugsy0nLeRfruTp0KAKbN2RAcDE
8bQNme/KHqZjwvJU6mdKUG8bXKZB1V4mGWNqZvzY5Q6oLAZI06guclJXR+YtzvBW
domtlw==
-----END CERTIFICATE-----"""

# Write CA certificate to file
ca_cert_path = os.path.join(os.path.dirname(__file__), "ca-cert.pem")
with open(ca_cert_path, "w") as f:
    f.write(ca_cert_content)

# Database connection
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "ssl_disabled": False,
        "ssl_ca": ca_cert_path
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
