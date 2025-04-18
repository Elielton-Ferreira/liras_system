from flask import Blueprint, render_template, request, redirect, flash, url_for
from controllers.vendas_controller import processar_venda
from models.venda import obter_vendas_com_itens
from models.vidro import listar_vidros_disponiveis

vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route('/vendas', methods=['GET', 'POST'])
def vendas():
    if request.method == 'POST':
        cliente = request.form.get('cliente')
        vendedor = request.form.get('vendedor')  # Novo campo
        mao_obra = float(request.form.get('mao_obra') or 0.0)
        itens = []

        for i in range(1, 51):  # permite até 50 itens dinâmicos
            vidro_id = request.form.get(f'vidro_id_{i}')
            quantidade = request.form.get(f'quantidade_{i}')
            preco = request.form.get(f'preco_m2_{i}')

            if vidro_id and quantidade and preco:
                quantidade = float(quantidade)
                if quantidade > 0:
                    itens.append({
                        'produto_id': int(vidro_id),
                        'tipo': 'vidro',
                        'quantidade': quantidade,
                        'preco_unitario': float(preco)
                    })

        if mao_obra > 0:
            itens.append({
                'produto_id': None,
                'tipo': 'mao_obra',
                'quantidade': 1,
                'preco_unitario': mao_obra
            })

        if itens:
            processar_venda(itens, cliente, vendedor)
            flash('Venda registrada com sucesso!', 'success')
            return redirect(url_for('vendas.vendas'))
        else:
            flash('Nenhum item válido informado.', 'danger')

    vidros = listar_vidros_disponiveis()
    return render_template('vendas.html', vidros=vidros)

@vendas_bp.route('/historico_vendas')
def historico_vendas():
    vendas = obter_vendas_com_itens()
    return render_template('historico_vendas.html', vendas=vendas)

# Rota para excluir venda
@vendas_bp.route('/venda/<int:venda_id>/excluir', methods=['POST'])
def excluir_venda(venda_id):
    from models.venda import excluir_venda_por_id

    excluir_venda_por_id(venda_id)
    flash('Venda excluída com sucesso!', 'success')
    return redirect(url_for('vendas.historico_vendas'))

# Rota (placeholder) para editar venda
@vendas_bp.route('/venda/<int:venda_id>/editar')
def editar_venda(venda_id):
    # Em breve: carregar dados da venda para edição
    flash(f'Edição da venda #{venda_id} ainda não implementada.', 'info')
    return redirect(url_for('vendas.historico_vendas'))
