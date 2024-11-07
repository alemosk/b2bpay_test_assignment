from django.db import models


class Transaction(models.Model):
    # The correct way to store transactions is to include both a source and a destination for funds.
    # However, this approach is not specified in the requirements.
    # In a real task, I would initiate a discussion on this topic to ensure the requirements are accurate.
    # Additionally, the amount should specify a currency to allow for correct cross-currency calculations.

    wallet = models.ForeignKey(
        'wallets.Wallet',
        related_name='transactions',
        # If the wallet contains any transactions, we can't allow it to be removed due to reporting reasons.
        on_delete=models.PROTECT,
    )
    # The task does not contain requirements for the maximum length of the transaction ID,
    # so we will use the length of UUID4 for transaction IDs.
    txid = models.CharField(
        max_length=36,
        unique=True,
    )

    amount = models.DecimalField(
        # The maximum length is not specified in the task, so we will use the MySQL DECIMAL maximum value (65).
        # https://dev.mysql.com/doc/refman/8.4/en/precision-math-decimal-characteristics.html
        max_digits=65,
        decimal_places=18,
        # we use index because we allow users to sort and filter data by this value.
        db_index=True,
    )

    class Meta:
        db_table = 'finances_transactions'
        ordering = ('id', )
