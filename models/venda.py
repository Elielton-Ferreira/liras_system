from models.database import conectar_bd

def criar_venda(cliente, vendedor):
    from datetime import datetime
    conn = conectar_bd()
    cursor = conn.cursor()

    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO vendas (data, cliente, vendedor) VALUES (?, ?, ?)", (data, cliente, vendedor))
    venda_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return venda_id

def adicionar_item_venda(venda_id, produto_id, tipo, quantidade, preco_unitario):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO itens_venda (venda_id, produto_id, tipo, quantidade, preco_unitario)
        VALUES (?, ?, ?, ?, ?)
    """, (venda_id, produto_id, tipo, quantidade, preco_unitario))
    conn.commit()
    conn.close()

def obter_vendas_com_itens():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vendas ORDER BY data DESC")
    vendas = cursor.fetchall()

    resultado = []

    for venda in vendas:
        cursor.execute("SELECT * FROM itens_venda WHERE venda_id = ?", (venda['id'],))
        itens = cursor.fetchall()

        total_area = 0
        total_m2 = 0
        mao_obra = 0

        for item in itens:
            subtotal = item['preco_unitario'] * item['quantidade']
            if item['tipo'] == 'vidro':
                total_area += item['quantidade']
                total_m2 += subtotal
            elif item['tipo'] == 'mao_obra':
                mao_obra += subtotal

        venda_dict = {
            'id': venda['id'],
            'data': venda['data'],
            'cliente': venda['cliente'],
            'vendedor': venda['vendedor'],
            'total_area': total_area,
            'total_m2': total_m2,
            'mao_obra': mao_obra,
            'total_geral': total_m2 + mao_obra
        }

        resultado.append(venda_dict)

    conn.close()
    return resultado

def excluir_venda_por_id(venda_id):
    conn = conectar_bd()
    cursor = conn.cursor()

    # Primeiro remove os itens associados
    cursor.execute("DELETE FROM itens_venda WHERE venda_id = ?", (venda_id,))
    # Depois remove a venda
    cursor.execute("DELETE FROM vendas WHERE id = ?", (venda_id,))

    conn.commit()
    conn.close()
