from flask import Flask, render_template, request, redirect, url_for
from database import get_connection
from datetime import datetime

app = Flask(__name__)


# ===== VALIDAÇÃO DE CPF =====
def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    if digito1 in (10, 11):
        digito1 = 0
    if digito1 != int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    if digito2 in (10, 11):
        digito2 = 0
    if digito2 != int(cpf[10]):
        return False

    return True


# ===== PAINEL =====
@app.route('/')
def painel():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM casas")
    casas = cursor.fetchall()

    casa_id = request.args.get('casa_id')
    mes = request.args.get('mes')
    periodo = request.args.get('periodo')
    busca = request.args.get('busca', '')

    filtros = []
    valores = []

    if casa_id:
        filtros.append("l.casa_id = %s")
        valores.append(casa_id)
    if mes:
        filtros.append("DATE_FORMAT(l.data_checkin, '%Y-%m') = %s")
        valores.append(mes)
    if periodo == 'ativas':
        filtros.append("l.data_checkout >= CURDATE()")
    elif periodo == 'passadas':
        filtros.append("l.data_checkout < CURDATE()")
    if busca:
        filtros.append("""
            EXISTS (
                SELECT 1 FROM hospedes h
                WHERE h.locacao_id = l.id
                AND h.is_responsavel = TRUE
                AND h.nome LIKE %s
            )
        """)
        valores.append(f'%{busca}%')

    where = "WHERE " + " AND ".join(filtros) if filtros else ""

    cursor.execute(f"""
        SELECT l.*, c.nome_casa,
               (SELECT nome FROM hospedes WHERE locacao_id = l.id AND is_responsavel = TRUE LIMIT 1) as responsavel
        FROM locacoes l
        JOIN casas c ON l.casa_id = c.id
        {where}
        ORDER BY l.data_checkin DESC
    """, valores)
    locacoes = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total FROM locacoes")
    total_reservas = cursor.fetchone()['total']

    cursor.execute("""
        SELECT COUNT(*) as total FROM locacoes l
        JOIN casas c ON l.casa_id = c.id
        WHERE c.nome_casa = 'Amiga'
    """)
    total_amiga = cursor.fetchone()['total']

    cursor.execute("""
        SELECT COUNT(*) as total FROM locacoes l
        JOIN casas c ON l.casa_id = c.id
        WHERE c.nome_casa = 'Casa Grande'
    """)
    total_casa_grande = cursor.fetchone()['total']

    cursor.execute("SELECT COALESCE(SUM(valor_total), 0) as total FROM locacoes")
    receita_total = cursor.fetchone()['total']

    conn.close()

    return render_template('painel.html',
        casas=casas,
        locacoes=locacoes,
        total_reservas=total_reservas,
        total_amiga=total_amiga,
        total_casa_grande=total_casa_grande,
        receita_total=receita_total,
        casa_id_selecionada=casa_id or '',
        mes_selecionado=mes or '',
        periodo_selecionado=periodo or '',
        busca=busca
    )


# ===== NOVA RESERVA =====
@app.route('/nova-reserva', methods=['GET', 'POST'])
def nova_reserva():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM casas")
    casas = cursor.fetchall()

    if request.method == 'POST':
        casa_id = request.form['casa_id']
        responsavel_nome = request.form['responsavel_nome']
        quantidade_hospedes = request.form['quantidade_hospedes']
        valor_total = request.form['valor_total']
        data_checkin = request.form['data_checkin']
        data_checkout = request.form['data_checkout']
        hora_checkin = request.form['hora_checkin']
        hora_checkout = request.form['hora_checkout']

        if data_checkout <= data_checkin:
            conn.close()
            return render_template('nova_reserva.html',
                casas=casas,
                erro="A data de check-out deve ser posterior à data de check-in."
            )

        cursor.execute("""
            SELECT COUNT(*) as total FROM locacoes
            WHERE casa_id = %s
            AND data_checkin < %s
            AND data_checkout > %s
        """, (casa_id, data_checkout, data_checkin))

        if cursor.fetchone()['total'] > 0:
            conn.close()
            return render_template('nova_reserva.html',
                casas=casas,
                erro="Esta casa já possui uma reserva neste período. Escolha outras datas ou outra casa."
            )

        cursor.execute("""
            INSERT INTO locacoes
                (casa_id, quantidade_hospedes, data_checkin, data_checkout,
                 hora_checkin, hora_checkout, valor_total)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (casa_id, quantidade_hospedes, data_checkin,
              data_checkout, hora_checkin, hora_checkout, valor_total))
        conn.commit()

        locacao_id = cursor.lastrowid
        conn.close()

        return redirect(url_for('add_hospedes',
                                locacao_id=locacao_id,
                                responsavel_nome=responsavel_nome))

    conn.close()
    return render_template('nova_reserva.html', casas=casas)


# ===== ADICIONAR HÓSPEDES =====
@app.route('/reserva/<int:locacao_id>/hospedes', methods=['GET', 'POST'])
def add_hospedes(locacao_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT l.*, c.nome_casa
        FROM locacoes l
        JOIN casas c ON l.casa_id = c.id
        WHERE l.id = %s
    """, (locacao_id,))
    locacao = cursor.fetchone()

    cursor.execute("SELECT * FROM hospedes WHERE locacao_id = %s", (locacao_id,))
    hospedes = cursor.fetchall()

    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form.get('cpf', '')
        faixa_etaria = request.form.get('faixa_etaria', '')
        modelo_carro = request.form.get('modelo_carro', '')
        placa_carro = request.form.get('placa_carro', '')

        if cpf and not validar_cpf(cpf):
            conn.close()
            conn2 = get_connection()
            cursor2 = conn2.cursor(dictionary=True)
            cursor2.execute("""
                SELECT l.*, c.nome_casa FROM locacoes l
                JOIN casas c ON l.casa_id = c.id WHERE l.id = %s
            """, (locacao_id,))
            locacao = cursor2.fetchone()
            cursor2.execute("SELECT * FROM hospedes WHERE locacao_id = %s", (locacao_id,))
            hospedes = cursor2.fetchall()
            conn2.close()
            return render_template('add_hospedes.html',
                locacao=locacao,
                hospedes=hospedes,
                locacao_id=locacao_id,
                responsavel_nome=nome,
                now=datetime.now(),
                erro_cpf="CPF inválido! Verifique o número digitado."
            )

        is_responsavel = len(hospedes) == 0

        cursor.execute("""
            INSERT INTO hospedes
                (locacao_id, nome, cpf, faixa_etaria, modelo_carro, placa_carro, is_responsavel)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (locacao_id, nome, cpf, faixa_etaria,
              modelo_carro, placa_carro, is_responsavel))
        conn.commit()

        return redirect(url_for('add_hospedes', locacao_id=locacao_id))

    responsavel_nome = request.args.get('responsavel_nome', '')

    conn.close()
    return render_template('add_hospedes.html',
        locacao=locacao,
        hospedes=hospedes,
        locacao_id=locacao_id,
        responsavel_nome=responsavel_nome,
        now=datetime.now()
    )


# ===== EXCLUIR HÓSPEDE =====
@app.route('/hospede/<int:hospede_id>/excluir')
def excluir_hospede(hospede_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT locacao_id FROM hospedes WHERE id = %s", (hospede_id,))
    hospede = cursor.fetchone()
    locacao_id = hospede['locacao_id']

    cursor.execute("DELETE FROM hospedes WHERE id = %s", (hospede_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('add_hospedes', locacao_id=locacao_id))


# ===== EXCLUIR RESERVA =====
@app.route('/reserva/<int:locacao_id>/excluir')
def excluir_reserva(locacao_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM hospedes WHERE locacao_id = %s", (locacao_id,))
    cursor.execute("DELETE FROM locacoes WHERE id = %s", (locacao_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('painel'))


# ===== AVALIAR RESERVA =====
@app.route('/reserva/<int:locacao_id>/avaliar', methods=['POST'])
def avaliar_reserva(locacao_id):
    conn = get_connection()
    cursor = conn.cursor()

    avaliacao = request.form.get('avaliacao')
    comentario = request.form.get('comentario', '')

    cursor.execute("""
        UPDATE locacoes
        SET avaliacao = %s, comentario = %s
        WHERE id = %s
    """, (avaliacao, comentario, locacao_id))
    conn.commit()
    conn.close()

    return redirect(url_for('add_hospedes', locacao_id=locacao_id))


# ===== PÁGINA DE RESERVAS =====
@app.route('/reservas')
def reservas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM casas")
    casas = cursor.fetchall()

    casa_id = request.args.get('casa_id')
    mes = request.args.get('mes')
    periodo = request.args.get('periodo')
    busca = request.args.get('busca', '')

    filtros = []
    valores = []

    if casa_id:
        filtros.append("l.casa_id = %s")
        valores.append(casa_id)
    if mes:
        filtros.append("DATE_FORMAT(l.data_checkin, '%Y-%m') = %s")
        valores.append(mes)
    if periodo == 'ativas':
        filtros.append("l.data_checkout >= CURDATE()")
    elif periodo == 'passadas':
        filtros.append("l.data_checkout < CURDATE()")
    if busca:
        filtros.append("""
            EXISTS (
                SELECT 1 FROM hospedes h
                WHERE h.locacao_id = l.id
                AND h.is_responsavel = TRUE
                AND h.nome LIKE %s
            )
        """)
        valores.append(f'%{busca}%')

    where = "WHERE " + " AND ".join(filtros) if filtros else ""

    cursor.execute(f"""
        SELECT l.*, c.nome_casa,
               (SELECT nome FROM hospedes WHERE locacao_id = l.id AND is_responsavel = TRUE LIMIT 1) as responsavel
        FROM locacoes l
        JOIN casas c ON l.casa_id = c.id
        {where}
        ORDER BY l.data_checkin DESC
    """, valores)
    locacoes = cursor.fetchall()

    conn.close()

    return render_template('reservas.html',
        casas=casas,
        locacoes=locacoes,
        casa_id_selecionada=casa_id or '',
        mes_selecionado=mes or '',
        periodo_selecionado=periodo or '',
        busca=busca
    )


if __name__ == '__main__':
    app.run(debug=True)