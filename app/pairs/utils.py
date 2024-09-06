from pairs.models import Tokens, Pools, TokenPools, DexNames, Blockchains


# 1. Создаем или находим токен
token_1, created = Tokens.objects.get_or_create(
    token_address='0xTokenAddress1',
    defaults={'token_name': 'Token1', 'token_symbol': 'TKN1'}
)

token_2, created = Tokens.objects.get_or_create(
    token_address='0xTokenAddress2',
    defaults={'token_name': 'Token2', 'token_symbol': 'TKN2'}
)

# 2. Находим или создаем блокчейн
blockchain, created = Blockchains.objects.get_or_create(
    name='Ethereum'
)

# 3. Находим или создаем DEX
dex, created = DexNames.objects.get_or_create(
    name='Uniswap',
    blockchain=blockchain
)

# 4. Создаем или находим пул ликвидности
pool, created = Pools.objects.get_or_create(
    pool_address='0xPoolAddress',
    token_1_id=token_1,
    token_2_id=token_2,
    dex_name=dex
)

# 5. Связываем токен с пулом в token_pools
token_pool_1, created = TokenPools.objects.get_or_create(
    token_id=token_1,
    pool_id=pool
)

token_pool_2, created = TokenPools.objects.get_or_create(
    token_id=token_2,
    pool_id=pool
)
