import hashlib
import os


# ---------------------------------------------------------
# 1) Hash do curso: soma dos valores ASCII
#    Serve só pra entender o conceito. A ordem das letras NÃO importa.
# ---------------------------------------------------------
def calcula_hash(senha):
    valor = 0
    for letra in senha:
        valor = valor + ord(letra)
    return valor


# ---------------------------------------------------------
# 2) Versão melhorada (djb2): a ordem das letras importa
#    Bom pra aprender, mas ainda é fraco (32 bits e muito rápido).
# ---------------------------------------------------------
def meu_hash(senha):
    valor = 5381                          # ponto de partida (não precisa ser zero)
    for letra in senha:
        valor = valor * 33 + ord(letra)   # multiplica e depois soma
        valor = valor % (2**32)           # mantém o número em 32 bits
    return valor


# ---------------------------------------------------------
# 3) Hash de verdade: PBKDF2 com salt (já vem no Python)
#    Lento de propósito, então a força bruta fica inviável.
# ---------------------------------------------------------
ITERACOES = 200_000


def hash_seguro(senha):
    salt = os.urandom(16)  # 16 bytes aleatórios, diferente a cada senha
    hash_bytes = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, ITERACOES)
    return salt.hex() + ":" + hash_bytes.hex()


def verifica(senha, guardado):
    salt_hex, hash_hex = guardado.split(":")
    salt = bytes.fromhex(salt_hex)
    novo = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, ITERACOES)
    return novo.hex() == hash_hex
  
if __name__ == "__main__":
    print("=== 1) Soma ASCII (anagramas dão o mesmo valor) ===")
    print("amor:", calcula_hash("amor"))
    print("roma:", calcula_hash("roma"))

    print("\n=== 2) djb2 (agora a ordem importa) ===")
    print("amor:", meu_hash("amor"))
    print("roma:", meu_hash("roma"))

    print("\n=== 3) PBKDF2 com salt ===")
    guardado = hash_seguro("Marcelo123")
    print("guardado:", guardado)
    print("senha certa  ->", verifica("Marcelo123", guardado))
    print("senha errada ->", verifica("marcelo123", guardado))

    print("\n=== Mesma senha, dois hashes diferentes (por causa do salt) ===")
    print(hash_seguro("Marcelo123") == hash_seguro("Marcelo123"))  # False
