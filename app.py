from flask import Flask, render_template, request, redirect
import json
import os
app = Flask(__name__)
FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            tasks = json.load(f)
            return tasks if isinstance(tasks, list) else []
    except (json.JSONDecodeError, IOError):
        return []

def save_tasks(tasks):
    try:
        with open(FILE, "w") as f:
            json.dump(tasks, f, indent=4)
    except IOError:
        print("Gagal menyimpan data ke file.")

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    deadline = request.form.get("deadline")

    if title: # Cek agar tidak kosong atau hanya spasi
        tasks = load_tasks()
        tasks.append({
            "title": title,
            "deadline": deadline,
            "done": False
        })
        save_tasks(tasks)
    return redirect("/")

@app.route("/done/<int:id>")
def done(id):
    tasks = load_tasks()
    if 0 <= id < len(tasks): # Validasi index
        tasks[id]["done"] = True
        save_tasks(tasks)
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    tasks = load_tasks()
    if 0 <= id < len(tasks): # Validasi index
        tasks.pop(id)
        save_tasks(tasks)
    return redirect("/")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)