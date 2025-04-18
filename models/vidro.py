from models.database import conectar_bd

def listar_vidros_disponiveis():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, preco_m2, area
        FROM vidros
        WHERE area > 0
    """)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def baixar_estoque(vidro_id, quantidade_m2):
    conn = conectar_bd()
    cursor = conn.cursor()

    # só baixa se houver estoque suficiente
    cursor.execute("SELECT area FROM vidros WHERE id = ?", (vidro_id,))
    resultado = cursor.fetchone()

    if resultado and resultado['area'] >= quantidade_m2:
        cursor.execute("""
            UPDATE vidros
            SET area = area - ?
            WHERE id = ?
        """, (quantidade_m2, vidro_id))
        conn.commit()

    conn.close()
