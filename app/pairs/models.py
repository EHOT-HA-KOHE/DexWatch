from django.db import models
from django.utils import timezone


class Blockchains(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Сеть")

    class Meta:
        db_table = "blockchain"

    def __str__(self) -> str:
        return self.name


class DexNames(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="DEX")
    address = models.CharField(max_length=150, unique=True, verbose_name="Адрес")
    blockchain = models.ForeignKey(
        to=Blockchains, on_delete=models.DO_NOTHING, verbose_name="Сеть"
    )

    class Meta:
        db_table = "dex_name"

    def __str__(self) -> str:
        return self.name


class Tokens(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")
    symbol = models.CharField(max_length=15, verbose_name="Символ")
    address = models.CharField(max_length=150, unique=True, verbose_name="Адрес")
    blockchain = models.ForeignKey(to=Blockchains, on_delete=models.DO_NOTHING, verbose_name="Сеть")

    class Meta:
        db_table = "token"

    def __str__(self) -> str:
        return f"{self.name} / {self.symbol} / {self.address}"


class Pools(models.Model):
    address = models.CharField(max_length=150, unique=True, verbose_name="Адрес")
    usd_price = models.DecimalField(max_digits=13, decimal_places=10, verbose_name="Цена USD")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    transactions = models.PositiveIntegerField(default=0, verbose_name='Количество транзакций')
    makers = models.PositiveIntegerField(default=0, verbose_name='Количество makers')
    volume = models.IntegerField(default=0, verbose_name='vol')
    price_change_5m = models.DecimalField(default=0, max_digits=15, decimal_places=2, verbose_name='Изменение цены 5 мин')
    price_change_1h = models.DecimalField(default=0, max_digits=15, decimal_places=2, verbose_name='Изменение цены 1 час')
    price_change_6h = models.DecimalField(default=0, max_digits=15, decimal_places=2, verbose_name='Изменение цены 6 часов')
    price_change_24h = models.DecimalField(default=0, max_digits=15, decimal_places=2, verbose_name='Изменение цены 24 часа')
    liquidity = models.IntegerField(default=0, verbose_name='Ликвидность')
    mcap = models.IntegerField(default=0, verbose_name='mcap')

    token_1 = models.ForeignKey(to=Tokens, on_delete=models.DO_NOTHING,
        related_name="pairs_as_token_1", verbose_name="Токен 1",)
    
    token_2 = models.ForeignKey(to=Tokens,on_delete=models.DO_NOTHING, 
        related_name="pairs_as_token_2", verbose_name="Токен 2",)
    
    blockchain = models.ForeignKey(to=Blockchains, on_delete=models.DO_NOTHING, verbose_name="Сеть")
    dex_name = models.ForeignKey(to=DexNames, on_delete=models.DO_NOTHING, verbose_name="DEX")

    @property
    def age(self):
        return timezone.now() - self.created_at

    @property
    def age_formatted(self):
        now = timezone.now()
        delta = now - self.created_at

        weeks, remainder = divmod(delta.days, 7)
        days, remainder = divmod(remainder, 1)
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        parts = []
        if weeks > 0:
            parts.append(f"{weeks}w")
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")

        return ' '.join(parts) if parts else '0m'

    class Meta:
        db_table = "pool"

    def __str__(self) -> str:
        return f"{self.address} / {self.token_1_id} / {self.token_2_id} / {self.dex_name}"


class TokenPools(models.Model):
    token = models.ForeignKey(
        to=Tokens, on_delete=models.DO_NOTHING, verbose_name="ID токена"
    )
    pool = models.ForeignKey(
        to=Pools, on_delete=models.DO_NOTHING, verbose_name="ID пула"
    )

    class Meta:
        db_table = "token_pool"
