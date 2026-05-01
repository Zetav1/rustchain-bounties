import sys
import os
import json

# Agregar el path del SDK para que Python pueda encontrarlo
sdk_path = r"C:\Users\B845K\Desktop\rustchain-bounties\sdk\python"
sys.path.append(sdk_path)

try:
    from rustchain_sdk.wallet import RustChainWallet
    
    # Crear una nueva wallet (128 bits = 12 palabras)
    wallet = RustChainWallet.create(strength=128)
    
    # Datos públicos
    address = wallet.address
    
    # Datos privados (Seed Phrase)
    seed = wallet.seed_phrase
    
    # Guardar localmente de forma persistente pero segura
    save_path = r"C:\Users\B845K\.openclaw\credentials\rustchain_wallet_zetav1.json"
    wallet_data = {
        "address": address,
        "seed_phrase": seed,
        "private_key_hex": wallet.private_key_hex
    }
    
    with open(save_path, "w") as f:
        json.dump(wallet_data, f, indent=4)
        
    print(f"WALLET_CREATED_SUCCESS")
    print(f"ADDRESS: {address}")
    print(f"PATH: {save_path}")

except Exception as e:
    print(f"ERROR: {str(e)}")
