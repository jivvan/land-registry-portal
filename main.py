from db import Database
from flask import Flask, send_from_directory, request, render_template, redirect, url_for

app = Flask(__name__, static_folder="static")

db = Database()


@app.get("/")
def index():
    return send_from_directory("templates", "index.html")


@app.get("/create_record")
def create_record():
    return send_from_directory("templates", "create_record.html")


@app.post("/submit_record")
def submit_record():
    data = request.form
    db.insert_land_record(data)
    return redirect(url_for('view_land_records'))


@app.get('/view_land_records')
def view_land_records():
    page = request.args.get('page', default=1, type=int)
    data = db.get_records(page)

    return render_template('view_land_records.html', land_records=data)


@app.get('/land_transaction')
def new_land_transaction():
    return send_from_directory('templates', 'land_transaction.html')


@app.post("/create_transaction")
def create_transaction():
    data = request.form
    db.transact_land(data)
    return redirect(url_for('view_land_records'))


@app.get('/land')
def land_details():
    id = request.args.get('id', default=1, type=int)
    page = request.args.get('page', default=1, type=int)
    print(db.get_transactions(id, page))
    return render_template('land.html', land_details={
        "details": db.get_record(id),
        "transactions": db.get_transactions(id, page)
    })


@app.get('/whole_geojson')
def get_whole_geojson():
    return db.get_geojson()


if __name__ == '__main__':
    app.run(debug=True)
