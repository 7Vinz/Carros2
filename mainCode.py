from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
itens = []  # lista que guarda os itens


@app.route("/")
def home():
    return send_from_directory(".", "Index.html")


@app.route("/itens", methods=["GET"])
def listar():
    return jsonify([{"nome": i["nome"], "validade": i["validade"].strftime("%d/%m/%Y")} for i in itens])


@app.route("/itens", methods=["POST"])
def cadastrar():
    dados = request.get_json()
    try:
        validade = datetime.strptime(dados["validade"], "%d/%m/%Y")
    except ValueError:
        return jsonify({"erro": "Data inválida"}), 400
    itens.append({"nome": dados["nome"], "validade": validade})
    return jsonify({"ok": True})


@app.route("/usar", methods=["POST"])
def usar():
    if not itens:
        return jsonify({"erro": "Nenhum item na lista"}), 400
    # percorre a lista procurando o item mais próximo da validade
    mais_proximo = itens[0]
    for item in itens:
        if item["validade"] < mais_proximo["validade"]:
            mais_proximo = item
    itens.remove(mais_proximo)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)
