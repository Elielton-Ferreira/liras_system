from models.venda import criar_venda, adicionar_item_venda
from models.produto import baixar_estoque as baixar_estoque_produto
from models.vidro import baixar_estoque as baixar_estoque_vidro

def processar_venda(itens, cliente, vendedor):
    venda_id = criar_venda(cliente, vendedor)

    for item in itens:
        adicionar_item_venda(
            venda_id,
            item['produto_id'],
            item['tipo'],
            item['quantidade'],
            item['preco_unitario']
        )

        if item['tipo'] == 'produto':
            baixar_estoque_produto(item['produto_id'], item['quantidade'])
        elif item['tipo'] == 'vidro':
            baixar_estoque_vidro(item['produto_id'], item['quantidade'])
    return venda_id
