def total(galleons, stalleons, knuts):
    return (galleons * 17 + stalleons) * 29 + knuts

coins = {"galleons": 100, "stalleons": 50, "knuts": 25}

print(total(**coins), "Knuts")