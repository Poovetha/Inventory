# Inventory App (Flask)

A simple web app to track products in different locations.

You can:
- Add/Edit/Delete Products
- Add/Edit/Delete Locations
- Record Product Movements (in, out, transfer)
- See the current balance per product at each location

## Get started
1) Make a virtual environment
- macOS/Linux
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
- Windows (PowerShell)
  - `py -3 -m venv .venv`
  - `.venv\Scripts\Activate`

2) Install packages
- `pip install -r requirements.txt`

3) Create a `.env` file (you can copy/paste this)
```
FLASK_ENV=development
DATABASE_URL=sqlite:///inventory.db
SECRET_KEY=dev-secret
```

4) Set up the database (first time only)
- `flask --app app db init`
- `flask --app app db migrate -m "init"`
- `flask --app app db upgrade`

5) (Optional) Add sample data
- `flask --app app seed`

6) Run the app
- `flask --app app run`
- Open `http://127.0.0.1:5000`

## How movements work (very short)
- Inbound: leave `from_location` empty
- Outbound: leave `to_location` empty
- Transfer: set both

## Change the database (optional)
- Keep SQLite by default. To use MySQL/Postgres, change `DATABASE_URL` in `.env` and install a driver:
  - MySQL: `pip install pymysql`
  - Postgres: `pip install psycopg2-binary`
- Then run: `flask --app app db upgrade`

## Folder guide
```
app/
  models.py   # database tables
  forms.py    # page forms
  views.py    # routes/pages
  templates/  # HTML templates
  static/     # CSS
```

## VS Code (optional)
- Open the folder, select the `.venv` interpreter, and run `flask --app app run` in the terminal.

---
Repository description:
"Simple Flask app to manage products, locations, and movements with a basic balance report. Easy setup with SQLite."

