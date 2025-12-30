from flask import Flask, render_template, request, redirect, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = "secret123"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "employees.db")

def get_db():
    return sqlite3.connect(DB_PATH)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------- ADMIN LOGIN ----------------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE username=? AND password=?", (user,pwd))
        admin = cur.fetchone()
        conn.close()

        if admin:
            session["admin"] = user
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/login")
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee")
    employees = cur.fetchall()
    conn.close()
    
    return render_template("dashboard.html", employees=employees)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

# ---------------- EMPLOYEE CRUD ----------------
@app.route("/add_page")
def add_page():
    if "admin" not in session:
        return redirect("/login")
    return render_template("add_employee.html")  # Correct template

@app.route("/add", methods=["POST"])
def add_employee():
    if "admin" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO employee(name,email,role,salary) VALUES (?,?,?,?)",
        (request.form["name"], request.form["email"],
         request.form["role"], request.form["salary"])
    )
    conn.commit()
    conn.close()
    return redirect("/dashboard")

@app.route("/view")
def view_employee():
    if "admin" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee")
    data = cur.fetchall()
    conn.close()
    return render_template("view_employee.html", employees=data)

@app.route("/delete/<int:id>")
def delete_employee(id):
    if "admin" not in session:
        return redirect("/login")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM employee WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

@app.route("/update/<int:id>")
def update_page(id):
    if "admin" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee WHERE id=?", (id,))
    emp = cur.fetchone()
    conn.close()
    return render_template("update_employee.html", emp=emp)

@app.route("/update", methods=["POST"])
def update_employee():
    if "admin" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE employee SET name=?,email=?,role=?,salary=?
        WHERE id=?
    """, (request.form["name"], request.form["email"],
          request.form["role"], request.form["salary"],
          request.form["id"]))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)
