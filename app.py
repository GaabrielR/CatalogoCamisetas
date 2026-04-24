from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, Camiseta, User, Favorito
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.secret_key = os.getenv("SECRET_KEY")

print(app.config.get("SQLALCHEMY_DATABASE_URI"))

db.init_app(app)

with app.app_context():
    db.create_all()

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@login_required
def index():
    camisetas = Camiseta.query.filter_by(user_id=current_user.id).all()
    return render_template("index.html", camisetas=camisetas)

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":

        imagem = request.files["imagem"]
        nome_arquivo = secure_filename(imagem.filename)
        imagem.save(os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo))

        camiseta = Camiseta(
            user_id=current_user.id,
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

        return redirect(url_for("index"))

    return render_template("create.html")

@app.route("/details/<int:id>")
@login_required
def details(id):
    camiseta = Camiseta.query.get_or_404(id)

    if camiseta.user_id != current_user.id:
        return redirect(url_for("index"))

    return render_template("details.html", camiseta=camiseta)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    camiseta = Camiseta.query.get_or_404(id)

    if camiseta.user_id != current_user.id:
        return redirect(url_for("index"))

@app.route("/delete/<int:id>")
@login_required
def delete(id):
    camiseta = Camiseta.query.get_or_404(id)

    if camiseta.user_id != current_user.id:
        return redirect(url_for("index"))

    db.session.delete(camiseta)
    db.session.commit()

    flash("Camiseta removida com sucesso!", "danger")
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]

        existing = User.query.filter_by(username=username).first()
        if existing:
            flash("Usuário já existe", "danger")
            return redirect(url_for("register"))

        password = generate_password_hash(request.form["password"])

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash("Usuário criado com sucesso!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if not user or not check_password_hash(user.password, request.form["password"]):
            flash("Usuário ou senha inválidos", "danger")
            return redirect(url_for("login"))

        login_user(user)
        return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/favoritar/<int:id>")
@login_required
def favoritar(id):

    fav = Favorito(user_id=current_user.id, camiseta_id=id)

    db.session.add(fav)
    db.session.commit()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)