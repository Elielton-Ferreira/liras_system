from models.database import conectar_bd

def baixar_estoque(produto_id, quantidade):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto_id))
    conn.commit()
    conn.close()
