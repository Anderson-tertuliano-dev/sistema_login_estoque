from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email_usuario", "").strip()
        senha = request.form.get("senha", "")

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        usuarios = cursor.fetchone()

        conn.close()

        if usuarios:
            return redirect(url_for("estoque"))
        else:
            return "Email ou senha incorretos."

    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        cpf = request.form.get("cpf")
        celular = request.form.get("celular")
        senha = request.form.get("senha")
        confirma_senha = request.form.get("confirma_senha")

        if senha != confirma_senha:
            return "ERRO: as senhas não conferem"

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, cpf, celular, senha) VALUES (?, ?, ?, ?, ?)",
                (nome, email, cpf, celular, senha)
            )
            conn.commit()
            return redirect(url_for("login"))

        except sqlite3.IntegrityError as e:
            if "email" in str(e):
                mensagem = "Erro: email já cadastrado."
            elif "cpf" in str(e):
                mensagem = "Erro: CPF já cadastrado."
            elif "celular" in str(e):
                mensagem = "Erro: telefone já cadastrado."
            else:
                mensagem = "Erro de integridade no cadastro."
        finally:
            conn.close()

        return mensagem

    return render_template("cadastro.html")


@app.route("/estoque", methods=["GET", "POST"])
def estoque():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    if request.method == "POST":
        produto = request.form.get("produto", "").strip()
        codigo = request.form.get("codigo", "").strip()
        quantidade = int(request.form.get("quantidade", 0))
        preco = float(request.form.get("preco", 0.0))

        try:
            cursor.execute(
                "INSERT INTO produtos (produto, codigo, quantidade, preco) VALUES(?, ?, ?, ?)", (
                    produto, codigo, quantidade, preco)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return "Erro codigo do produto já existe!"

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()

    return render_template("estoque.html", produtos=produtos)


if __name__ == "__main__":
    app.run(debug=True)
