from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# Définition du modèle de tâche avec chaque attributs
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    with app.app_context():
        # Trier les tâches par ordre de création décroissante
        tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)


@app.route('/create', methods=['POST'])
def create():
    with app.app_context(): 
        # Récupère les données du formulaire
        title = request.form['title']
        description = request.form['description']
        
        # Crée une nouvelle instance de tâche
        task = Task(title=title, description=description)
        
        # Ajoute la tâche à la base de données
        db.session.add(task)
        db.session.commit()
    
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    with app.app_context():  # Crée le contexte de l'application
        # Récupère la tâche correspondant à l'ID
        task = Task.query.get_or_404(id)
        
        # Inverse l'état de complétion de la tâche
        task.completed = not task.completed
        
        # Enregistre les modifications dans la base de données
        db.session.commit()
    
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    with app.app_context():  # Crée le contexte de l'application
        # Récupère la tâche correspondant à l'ID
        task = Task.query.get_or_404(id)
        
        # Supprime la tâche de la base de données
        db.session.delete(task)
        db.session.commit()
    
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():  # Crée le contexte de l'application
        # Crée les tables dans la base de données si elles n'existent pas encore
        db.create_all()
    
    # Lance l'application Flask en mode de débogage
    app.run(debug=True)
