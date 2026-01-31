def formatar_valor(valor_raw):
    try:
        valor = int(float(valor_raw))

        # remove zeros extras tipo 31000000 → 310000
        while valor > 2000000:
            valor = valor // 10

        if valor >= 1000000:
            milhoes = valor // 1000000
            return f"{milhoes} milhão" if milhoes == 1 else f"{milhoes} milhões"

        mil = valor // 1000
        return f"{mil} mil"

    except:
        return None
