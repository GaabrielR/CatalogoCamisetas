from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, Camiseta
import os
from werkzeug.utils import secure_filename, generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

print(app.config.get("SQLALCHEMY_DATABASE_URI"))

db.init_app(app)

with app.app_context():
    db.create_all()

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/")
def index():
    user = current_user()

    if not user:
        return redirect(url_for("login"))

    query = Camiseta.query.filter_by(user_id=user.id)

    busca = request.args.get("busca", "")
    time = request.args.get("time", "")
    marca = request.args.get("marca", "")

    query = Camiseta.query

    if busca:
        query = query.filter(
            (Camiseta.time.contains(busca)) |
            (Camiseta.jogador.contains(busca))
        )

    if time:
        query = query.filter_by(time=time)

    if marca:
        query = query.filter_by(marca=marca)

    camisetas = query.order_by(Camiseta.created_at.desc()).all()

    return render_template("index.html", camisetas=camisetas)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        imagem = request.files.get("imagem")
        nome_arquivo = None

        if imagem and imagem.filename:
            nome_arquivo = secure_filename(imagem.filename)
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo)
            imagem.save(caminho)

        user = current_user()

        camiseta = Camiseta(
            time=request.form["time"],
            pais=request.form["pais"],
            modalidade=request.form["modalidade"],
            temporada=request.form["temporada"],
            tipo=request.form["tipo"],
            marca=request.form["marca"],
            tamanho=request.form["tamanho"],
            jogador=request.form.get("jogador"),
            numero=request.form.get("numero"),
            condicao=request.form["condicao"],
            observacoes=request.form.get("observacoes"),
            imagem=nome_arquivo
        )

        db.session.add(camiseta)
        db.session.commit()

        flash("Camiseta cadastrada com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("create.html")

@app.route("/details/<int:id>")
def details(id):
    camiseta = Camiseta.query.get_or_404(id)
    return render_template("details.html", camiseta=camiseta)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    camiseta = Camiseta.query.get_or_404(id)

    if request.method == "POST":
        camiseta.time = request.form["time"]
        camiseta.pais = request.form["pais"]
        camiseta.modalidade = request.form["modalidade"]
        camiseta.temporada = request.form["temporada"]
        camiseta.tipo = request.form["tipo"]
        camiseta.marca = request.form["marca"]
        camiseta.tamanho = request.form["tamanho"]
        camiseta.jogador = request.form.get("jogador")
        camiseta.numero = request.form.get("numero")
        camiseta.condicao = request.form["condicao"]
        camiseta.observacoes = request.form.get("observacoes")

        db.session.commit()

        flash("Camiseta atualizada com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", camiseta=camiseta)

@app.route("/delete/<int:id>")
def delete(id):
    camiseta = Camiseta.query.get_or_404(id)
    db.session.delete(camiseta)
    db.session.commit()

    flash("Camiseta removida com sucesso!", "danger")
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            session["user_id"] = user.id
            return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

def current_user():
    if "user_id" in session:
        return User.query.get(session["user_id"])
    return None

@app.route("/favoritar/<int:id>")
def favoritar(id):
    user = current_user()

    fav = Favorito(user_id=user.id, camiseta_id=id)
    db.session.add(fav)
    db.session.commit()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)