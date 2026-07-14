# Ets. Plastique Recyclage — Application de Gestion Achat/Vente de Matières Plastiques

Application web complète (Django + MySQL + Bootstrap 5) pour gérer l'activité
d'achat et de vente de matières plastiques : achats, ventes, paiements,
chèques, stock, clients, fournisseurs, facturation PDF et tableau de bord.

## 1. Stack technique

| Couche       | Technologie                                   |
|--------------|------------------------------------------------|
| Frontend     | HTML5, Bootstrap 5, FontAwesome, Chart.js       |
| Backend      | Django 6 (Python)                               |
| Base de données | MySQL (bascule SQLite possible pour tester)  |
| PDF          | ReportLab (factures, exports)                   |
| Excel        | openpyxl (exports)                              |

## 2. Installation

```bash
# 1. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer l'environnement
cp .env.example .env
# -> éditez .env : identifiants MySQL, clé secrète, nom de l'entreprise...

# 4. Créer la base MySQL (si vous n'utilisez pas SQLite)
mysql -u root -p -e "CREATE DATABASE plastique_erp CHARACTER SET utf8mb4;"

# 5. Appliquer les migrations
python manage.py migrate

# 6. Créer le compte administrateur (votre père)
python manage.py createsuperuser
# -> lors de la création, le rôle par défaut est "employe" ; passez-le en
#    "admin" depuis /admin/ (champ Role) ou via le shell :
#    python manage.py shell -c "from accounts.models import User; u=User.objects.get(username='VOTRE_LOGIN'); u.role='admin'; u.is_superuser=True; u.is_staff=True; u.save()"

# 7. Lancer le serveur
python manage.py runserver
```

Ouvrez ensuite **http://127.0.0.1:8000/** et connectez-vous.

### Tester rapidement sans MySQL

Dans `.env`, mettez `USE_SQLITE=True` : l'application bascule automatiquement
sur une base SQLite locale (`db.sqlite3`), pratique pour une démo rapide.

### Gérer la base avec phpMyAdmin

Un fichier `docker-compose.yml` est fourni pour lancer MySQL **et**
phpMyAdmin ensemble (nécessite [Docker](https://docs.docker.com/get-docker/)) :

```bash
docker compose up -d
```

- MySQL est exposé sur `127.0.0.1:3306` (mêmes identifiants que votre `.env`)
- phpMyAdmin est accessible sur **http://127.0.0.1:8080**
  → serveur : `mysql`, utilisateur/mot de passe : ceux de `DB_USER` / `DB_PASSWORD`
    dans votre `.env` (ou `root` / `DB_ROOT_PASSWORD` pour un accès complet)

Une fois les conteneurs lancés, appliquez les migrations Django normalement
(`python manage.py migrate`) : phpMyAdmin et Django pointent vers la même base.

Pour arrêter : `docker compose down` (les données restent dans le volume
`mysql_data` ; ajoutez `-v` pour tout effacer).

**Sans Docker** : installez phpMyAdmin via votre distribution (`apt install
phpmyadmin` sur Ubuntu/Debian) ou un pack comme XAMPP/WAMP/MAMP, puis
renseignez les mêmes `DB_HOST` / `DB_USER` / `DB_PASSWORD` que dans votre
`.env` lors de la connexion.

## 3. Fonctionnalités livrées

**Authentification & rôles**
- Deux rôles : Administrateur / Employé (modèle `User` personnalisé)
- Page de connexion, déconnexion, gestion des employés (admin uniquement)
- Toutes les pages sont protégées (middleware de connexion obligatoire)

**Achats** (`/achats/`)
- Formulaire complet (fournisseur, matière, **quantité** en Kg, prix, date,
  n° de bon, upload photo du bon de pesée, observations)
- Calcul automatique du montant : Quantité × Prix = Total (JS en temps réel
  + recalcul serveur garanti à l'enregistrement)
- **Facture PDF générée automatiquement** pour chaque achat (numérotée
  `BA-AAAA-NNNN`), téléchargeable depuis la liste ou la fiche achat
- Paiement (espèces / chèque / mixte) avec **plusieurs chèques** par
  paiement (numéro, banque, montant, date d'encaissement, photo, statut)
- Statut automatique : Non payé / En cours / Payé

**Ventes** (`/ventes/`)
- Même principe que les achats (quantité en Kg × prix = total)
- **Facture PDF générée automatiquement** pour chaque vente (numérotée
  `FA-AAAA-NNNN`) — logo, entreprise, client, produit, quantité, prix,
  total, date, numéro de facture — téléchargeable et imprimable
- Même système de paiement multi-chèques que les achats

**Matières** (`/matieres/`)
- CRUD des types de matières (PET Bleu, HDPE, PP...), utilisées dans les
  listes déroulantes achats/ventes

**Clients & Fournisseurs** (`/partenaires/`)
- Listes avec total acheté / payé / restant, recherche par nom
- Fiche détail avec historique complet des ventes/achats liés

**Chèques** (`/cheques/`)
- Vue "Chèques à payer" (issus des achats) et "Chèques à encaisser" (issus
  des ventes), avec filtre Aujourd'hui / Cette semaine / Ce mois

**Stock** (`/stock/`)
- Calcul automatique par matière : Stock = Quantité achetée − Quantité
  vendue (toutes les quantités sont saisies directement en Kg)
- Alerte visuelle si le stock passe sous le seuil configuré

**Recherche globale** (`/recherche/`)
- Recherche unique sur clients, fournisseurs, matières, achats et ventes

**Exports** (`/exports/`)
- Export PDF et Excel pour Achats, Ventes, Clients, Fournisseurs, Stock

**Tableau de bord** (`/dashboard/`)
- Cartes KPI : achats/ventes du jour, chiffre d'affaires, dépenses, profit,
  chèques en attente, créances clients, dettes fournisseurs, stock, etc.
- Graphiques Chart.js : évolution achats/ventes, répartition des matières,
  top clients, top fournisseurs
- Notifications automatiques (cloche) : chèques à échéance proche, stock
  faible, factures non réglées

**Design**
- Palette bleu / blanc / gris clair inspirée des ERP modernes
- Sidebar moderne, navbar, icônes FontAwesome, tableaux professionnels
- **Mode sombre** (bouton lune dans la navbar)
- Responsive (PC, tablette, mobile)

**Sécurité**
- Mots de passe hachés (mécanisme Django standard, PBKDF2)
- Rôles et permissions (décorateur `@admin_required` pour les pages admin)
- Historique natif via l'admin Django (`django.contrib.admin` journalise
  les actions) — voir section "Pour aller plus loin" pour un logging dédié

## 4. Structure du projet

```
plastique_erp/
├── config/          # Réglages Django, urls.py principal
├── accounts/        # Utilisateurs, rôles, connexion
├── core/            # Template de base, middleware, CSS/JS partagés
├── matieres/         # Types de matières plastiques
├── partenaires/      # Clients & Fournisseurs
├── achats/           # Achats + paiements + chèques
├── ventes/           # Ventes + paiements + chèques + facture PDF
├── stock/            # Calcul du stock
├── dashboard/        # KPIs, graphiques, notifications
├── cheques/          # Chèques à payer / à encaisser
├── recherche/        # Recherche globale
├── exports/          # Exports PDF / Excel
└── requirements.txt
```

## 5. Pour aller plus loin (non couvert dans cette première version)

Le cahier des charges est très large ; cette base couvre l'essentiel du
flux métier et est testée de bout en bout (création d'achats/ventes,
paiements multi-chèques, facture PDF, exports, tableau de bord). Quelques
compléments utiles pour une mise en production :

- **Historique des actions (logs)** détaillé par action métier (au-delà de
  l'admin Django) — un modèle `JournalAction` + middleware dédié.
- **Sauvegarde automatique de la base de données** — à planifier via cron
  (`mysqldump`) ou un service managé selon votre hébergeur.
- **Notifications temps réel** (actuellement calculées à chaque requête ;
  un job planifié + emails/SMS peut être ajouté).
- **Tests automatisés** (pytest/unittest) pour couvrir les cas limites.

N'hésitez pas à revenir vers moi pour prioriser et développer l'un de ces
points, ou pour ajuster une fonctionnalité existante.

## 6. Déploiement en production (VPS + nom de domaine)

Cette section explique comment mettre l'application en ligne avec un vrai
nom de domaine, sur un VPS (serveur privé virtuel). Les fichiers modèles
`deploy/gunicorn.service` et `deploy/nginx_plastique_erp.conf` sont fournis
dans le projet.

### 6.1 Acheter un nom de domaine
N'importe quel registrar convient : Namecheap, OVH, GoDaddy... Comptez
environ 80-120 DH/an pour un `.com`.

### 6.2 Louer un VPS
Fournisseurs courants et abordables : **Contabo**, **Hostinger VPS**,
**OVH VPS** (à partir de ~40-60 DH/mois). Choisissez **Ubuntu 22.04** comme
système d'exploitation.

### 6.3 Pointer le domaine vers le VPS
Chez votre registrar, dans la gestion DNS du domaine, ajoutez :
- Un enregistrement **A** : `@` → IP du VPS
- Un enregistrement **A** : `www` → IP du VPS

(La propagation peut prendre de quelques minutes à quelques heures.)

### 6.4 Se connecter au VPS et installer les prérequis

```bash
ssh root@IP_DU_VPS

apt update && apt upgrade -y
apt install -y python3-venv python3-pip nginx certbot python3-certbot-nginx unzip git

# Docker (pour MySQL + phpMyAdmin, comme en local)
curl -fsSL https://get.docker.com | sh
```

### 6.5 Créer un utilisateur dédié (bonne pratique de sécurité)

```bash
adduser django
usermod -aG docker django
su - django
```

### 6.6 Déposer le projet sur le VPS

Depuis votre machine, envoyez le zip au VPS :

```bash
scp plastique_erp.zip django@IP_DU_VPS:/home/django/
```

Puis sur le VPS :
```bash
cd /home/django
unzip plastique_erp.zip
cd plastique_erp
```

### 6.7 Lancer MySQL + phpMyAdmin (Docker)

```bash
cp .env.example .env
nano .env
```
Configurez notamment :
```
USE_SQLITE=False
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=votredomaine.com,www.votredomaine.com
DB_NAME=plastique_erp
DB_USER=plastique_user
DB_PASSWORD=un_mot_de_passe_fort
DB_ROOT_PASSWORD=un_autre_mot_de_passe_fort
```

```bash
docker compose up -d
```

phpMyAdmin sera accessible sur `http://IP_DU_VPS:8080` (pensez à limiter
l'accès à ce port dans votre pare-feu, ou à le fermer une fois les vérifs
terminées).

### 6.8 Installer l'application Python

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 6.9 Lancer Django avec Gunicorn (service permanent)

Adaptez les chemins dans `deploy/gunicorn.service` si besoin, puis :

```bash
sudo cp deploy/gunicorn.service /etc/systemd/system/plastique_erp.service
sudo systemctl daemon-reload
sudo systemctl start plastique_erp
sudo systemctl enable plastique_erp
sudo systemctl status plastique_erp   # doit afficher "active (running)"
```

### 6.10 Configurer Nginx

Remplacez `votredomaine.com` par votre vrai domaine dans
`deploy/nginx_plastique_erp.conf`, puis :

```bash
sudo cp deploy/nginx_plastique_erp.conf /etc/nginx/sites-available/plastique_erp
sudo ln -s /etc/nginx/sites-available/plastique_erp /etc/nginx/sites-enabled/
sudo nginx -t        # vérifie la config
sudo systemctl restart nginx
```

À ce stade, `http://votredomaine.com` doit déjà afficher l'application.

### 6.11 Activer le HTTPS (certificat gratuit Let's Encrypt)

```bash
sudo certbot --nginx -d votredomaine.com -d www.votredomaine.com
```

Certbot configure automatiquement Nginx pour rediriger vers HTTPS et
renouvelle le certificat tout seul.

### 6.12 Mises à jour futures

```bash
cd /home/django/plastique_erp
source venv/bin/activate
git pull            # ou re-uploader le zip
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart plastique_erp
```

## 7. Site bilingue Français / Arabe (RTL)

L'application est entièrement traduite en **français** et en **arabe**, avec
bascule automatique de la mise en page en RTL (droite-à-gauche) pour l'arabe.

- Sélecteur de langue disponible sur la page de connexion et dans la barre
  supérieure (icône 🌐) une fois connecté.
- Les URLs sont préfixées par la langue : `/fr/...` ou `/ar/...`.
- Le sens de lecture (`dir="rtl"`), la police (Noto Kufi Arabic) et la
  disposition (barre latérale à droite, textes alignés à droite...) basculent
  automatiquement en arabe.

### Ajouter ou corriger des traductions

Les traductions se trouvent dans `locale/ar/LC_MESSAGES/django.po` (déjà
compilé en `django.mo`, prêt à l'emploi). Pour modifier une traduction ou en
ajouter de nouvelles après avoir modifié le code :

```bash
python manage.py makemessages -l ar --no-location
# éditez locale/ar/LC_MESSAGES/django.po (modifiez les lignes msgstr "...")
python manage.py compilemessages
```

⚠️ `compilemessages` nécessite l'outil `gettext` installé sur la machine :
- **Ubuntu/Debian** : `sudo apt install gettext`
- **Windows** : téléchargez gettext depuis https://mlocati.github.io/articles/gettext-iconv-windows.html
- **macOS** : `brew install gettext`

Si vous ne modifiez pas les traductions, aucune installation supplémentaire
n'est nécessaire : le fichier `django.mo` fourni est déjà prêt à l'emploi.

## 8. Statuts des chèques (En attente / Encaissé / Annulé)

Chaque chèque (achat ou vente) a maintenant 3 statuts possibles :
- **En attente** : chèque remis, pas encore passé en banque
- **Encaissé** : chèque bien passé ("daz")
- **Annulé** : chèque rejeté/annulé — **son montant est automatiquement
  retiré du total payé**, donc le reste à payer/recevoir de l'achat ou de
  la vente augmente à nouveau du montant de ce chèque

Ces statuts peuvent être changés à tout moment :
- Depuis **Chèques à payer** / **Chèques à encaisser** (boutons ✓ et ✗)
- Depuis la fiche détail d'un achat ou d'une vente (menu ⋯ à côté de
  chaque chèque, avec options Marquer encaissé / Remettre en attente /
  Annuler le chèque)

## 9. Relevé groupé de factures (PDF)

Dans les listes **Achats** et **Ventes**, vous pouvez maintenant sélectionner
plusieurs factures via des cases à cocher (une case "tout sélectionner" est
disponible en haut de la colonne). Un compteur affiche en temps réel le
nombre de factures sélectionnées et leur **total combiné**.

En cliquant sur **"Générer un relevé groupé (PDF)"**, un document PDF est
généré avec :
- Le détail de chaque facture sélectionnée (numéro, client/fournisseur,
  matière, date, quantité, montant)
- Un **total général** en bas du document

Utile par exemple pour donner à un client ou un fournisseur un récapitulatif
de plusieurs factures en une seule fois.
# plastique_erp
