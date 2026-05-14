import requests
import os

API_KEY = "PDZHGSS5NYSV6W25H2JH7IH7IBI7JABF1D"

SAVE_DIR = "etherscan_contracts"
os.makedirs(SAVE_DIR, exist_ok=True)

CONTRACT_ADDRESSES = [
    # --- ERC20 Tokens (OpenZeppelin-based) ---
    "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
    "0x6B175474E89094C44Da98b954EedeAC495271d0F",  # DAI
    "0x514910771AF9Ca656af840dff83E8264EcF986CA",  # LINK
    "0xC02aaA39b223FE8D0A0E5C4F27eAD9083C756Cc2",  # WETH

    # --- ERC721 NFTs ---
    "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",  # BAYC
    "0xed5af388653567af2f388e6224dc7c4b3241c544",  # Azuki
    "0x8a90cab2b38dba80c64b7734e58ee1db38b8992e",  # Doodles

    # --- DeFi Protocols (complex logic) ---
    "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",  # Uniswap V2 Factory
    "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",  # Uniswap V3 Positions NFT
    "0x7Be8076f4EA4A4AD08075C2508e481d6C946D12b",  # OpenSea Seaport
    "0x3f5CE5FBFe3E9af3971dD833D26BA9b5C936f0bE",  # Binance Hot Wallet (many verified contracts)
    "0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5",  # Aave LendingPool V2
    "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B",  # Compound Comptroller
    "0x1F98431c8aD98523631AE4a59f267346ea31F984",  # Uniswap V3 Factory

    # --- Governance / DAO ---
    "0x5e4be8Bc9637f0EAA1A755019e06A68ce081D58F",  # Optimism Governance
    "0x9e1c6f3c2b6f2d7f6c2e3c3f3f3c3c3c3c3c3c3c",  # ENS DAO (example)
    
    # --- Access Control / Security Patterns ---
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",  # Uniswap Router (Ownable + Reentrancy patterns)
    "0x0000000000000000000000000000000000000000",  # (placeholder for testing)

    # --- Stablecoins (good structure) ---
    "0x0000000000085d4780B73119b644AE5ecd22b376",  # TUSD
    "0x4fabb145d64652a948d72533023f6e7a623c7c53",  # BUSD

    # --- Multisig / Escrow / Wallets ---
    "0x863b49ae97c3d2a87fd43186dfd921f42783c853",  # Gnosis Safe Proxy
    "0x34d402f14d58e001d8efbe6585051bf9706aa064",  # Gnosis Safe MasterCopy

    # --- Bridges / Cross-chain ---
    "0x3ee18b2214aff97000d974cf647e7c347e8fa585",  # Wormhole Bridge
    "0x98f3c9e6e3fAce36bAAd05FE09d375Ef1464288B",  # Multichain Router

    # --- Random Verified Contracts (diversity) ---
    "0x0d8775f648430679a709e98d2b0cb6250d2887ef",  # BAT
    "0x1111111254fb6c44bac0bed2854e76f90643097d",  # 1inch Router
    "0x6810e776880c02933d47db1b9fc05908e5386b96",  # GNO
    "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e",  # YFI
]


for addr in CONTRACT_ADDRESSES:

    url = (
        f"https://api.etherscan.io/v2/api"
        f"?chainid=1"
        f"&module=contract"
        f"&action=getsourcecode"
        f"&address={addr}"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)

    try:
        resp = response.json()
    except Exception as e:
        print("JSON Decode Error:", e)
        continue

    print(resp)

    if resp["status"] != "1":
        print("API Error:", resp["result"])
        continue

    result = resp["result"][0]

    source = result.get("SourceCode", "")
    name = result.get("ContractName", addr)

    if not source:
        print(f"No source code for {addr}")
        continue

    # Handle wrapped JSON contracts
    if source.startswith("{{") and source.endswith("}}"):
        source = source[1:-1]

    # Safe filename
    safe_name = "".join(c for c in name if c.isalnum() or c in ("_", "-"))

    filename = f"{safe_name}_{addr}.sol"
    path = os.path.join(SAVE_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(source)

    print(f"Saved: {path}")