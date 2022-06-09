""" Adapted from https://github.com/miguelgrinberg/flask-tables """

import logging

from flask import Flask, render_template, request
from common.config import config
from common.orm import Session, Valuations, orm_to_dict
from sqlalchemy import or_

logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config.from_object(config)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Find the intrinsic value of stocks")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/greenwald")
def greenwald():
    return render_template("greenwald.html", title="Greenwald")

@app.route("/damodaran")
def damodaran():
    return render_template("damodaran.html", title="Damodaran")

@app.route("/margin_of_safety")
def margin_of_safety():
    return render_template("margin_of_safety.html", title="Margin of Safety")

@app.route("/payback")
def payback():
    return render_template("payback.html", title="Payback")

@app.route("/ten_cap")
def ten_cap():
    return render_template("ten_cap.html", title="Ten Cap")

@app.route("/api/data/", methods=["GET", "POST"])
def data():

    group = request.args.get("group")
    upside = request.args.get("upside")

    with Session() as session:

        query = session.query(Valuations)

        if upside == '1':
             query = query.filter(
                 Valuations.margin_of_safety >= 0
             )

        if group != "all":
            query = query.filter(
                Valuations.business_category == group
            )

        # search filter
        search = request.args.get("search[value]")
        if search:
            query = query.filter(
                or_(
                    Valuations.company.ilike(f"%{search}%"),
                )
            )
        total_filtered = query.count()

        # sorting
        order = []
        i = 0
        while True:
            col_index = request.args.get(f"order[{i}][column]")
            if col_index is None:
                break
            col_name = request.args.get(f"columns[{col_index}][data]")
            # if col_name not in ['name', 'age', 'email']:
            #     col_name = 'name'
            descending = request.args.get(f"order[{i}][dir]") == "desc"
            col = getattr(Valuations, col_name)
            if descending:
                col = col.desc()
            order.append(col)
            i += 1
        if order:
            query = query.order_by(*order)

        # pagination
        start = request.args.get("start", type=int)
        length = request.args.get("length", type=int)
        query = query.offset(start).limit(length)

        # response
        return {
            "data": [orm_to_dict(valuation) for valuation in query],
            "recordsFiltered": total_filtered,
            "recordsTotal": query.count(),
            "draw": request.args.get("draw", type=int),
        }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
