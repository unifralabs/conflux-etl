class EntityType:
    BLOCK = 'block'
    TRANSACTION = 'transaction'
    RECEIPT = 'receipt'
    LOG = 'log'
    TOKEN_TRANSFER = 'token_transfer'
    CONTRACT = 'contract'
    TOKEN = 'token'

    ALL_FOR_STREAMING = [BLOCK, TRANSACTION, LOG, TOKEN_TRANSFER, CONTRACT, TOKEN]
    ALL_FOR_INFURA = [BLOCK, TRANSACTION, LOG, TOKEN_TRANSFER]
