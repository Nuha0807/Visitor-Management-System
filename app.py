from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "super_secret_key"


# ---------------- MOCK USERS ----------------
users = {
    "admin@company.com": {
        "password": "admin123",
        "role": "Admin",
        "name": "Admin User"
    },
    "security@company.com": {
        "password": "security123",
        "role": "Security",
        "name": "Security User"
    },
    "reception@company.com": {
        "password": "reception123",
        "role": "Reception",
        "name": "Reception User"
    }
}


# ---------------- HOME ----------------
@app.route("/")
def home():
    if "email" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    # If already logged in
    if "email" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        user = users.get(email)

        # Validate credentials
        if user and user["password"] == password and user["role"] == role:
            session["email"] = email
            session["name"] = user["name"]
            session["role"] = user["role"]

            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Email / Password / Role")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("login"))

    user_info = {
        "name": session.get("name"),
        "role": session.get("role")
    }

    data = {
        "total_visitors": 145,
        "checked_in": 12,
        "checked_out": 133,
        "pending_approvals": 3
    }

    return render_template("dashboard.html", user=user_info, data=data)


# ---------------- VISITORS ----------------
@app.route("/visitors")
def visitors():
    if "email" not in session:
        return redirect(url_for("login"))

    return render_template("visitor.html",
            user={"name": session.get("name"),
            "role": session.get("role")})


# ---------------- CHECK IN ----------------
@app.route("/checkin")
def checkin():
    if "email" not in session:
        return redirect(url_for("login"))

    return "<h2>Visitor Check-In Page</h2>"


# ---------------- CHECK OUT ----------------
@app.route("/checkout")
def checkout():
    if "email" not in session:
        return redirect(url_for("login"))

    return "<h2>Visitor Check-Out Page</h2>"


# ---------------- REPORTS ----------------
@app.route("/reports")
def reports():
    if "email" not in session:
        return redirect(url_for("login"))

    return render_template("report.html",
                    user={"name": session.get("name"),
                    "role": session.get("role")})


# ---------------- USERS ----------------
@app.route("/users")
def users_page():
    if "email" not in session:
        return redirect(url_for("login"))

    return render_template("users.html",
                user={"name": session.get("name"),
                "role": session.get("role")})


# ---------------- SETTINGS ----------------
@app.route("/settings")
def settings():
    if "email" not in session:
        return redirect(url_for("login"))

    return render_template("settings.html",
            user={"name": session.get("name"),
            "role": session.get("role")})


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)