from flask import Flask, render_template, request, url_for, redirect
from Runner import Runner

app = Flask(__name__)

last_result = None
last_inputs = None

@app.route("/")
def home():
    return render_template("index.html", has_results=last_result is not None, inputs=last_inputs)


@app.route("/analysis", methods=["GET", "POST"])
def analysis():

    global last_result
    global last_inputs
    if request.method == "GET":
        return render_template("results.html", inputs=last_inputs)

    name = request.form["company_name"]
    industry = request.form["industry"]

    revenue = float(request.form["revenue"])    
    cogs = float(request.form["cogs"])
    sga = float(request.form["sga"])
    marketing = float(request.form["marketing"])
    rd = float(request.form["rd"])
    depreciation = float(request.form["depreciation"])
    amortization = float(request.form["amortization"])
    current_assets = float(request.form["current_assets"])
    liabilities = float(request.form["current_liabilities"])
    non_cash = float(request.form["non_cash"])
    change_wc = float(request.form["change_wc"])
    capex = float(request.form["capex"])

    runner = Runner()

    result = runner.analyze_company(
        name=name,
        industry=industry,
        revenue=revenue,
        cogs=cogs,
        sga=sga,
        marketing=marketing,
        rd=rd,
        depreciation=depreciation,
        amortization=amortization,
        current_assets=current_assets,
        liabilities=liabilities,
        non_cash=non_cash,
        change_wc=change_wc,
        capex=capex
    )

    last_inputs = {
        "name": name,
        "industry": industry,
        "revenue": revenue,
        "cogs": cogs,
        "sga": sga,
        "marketing": marketing,
        "rd": rd,
        "depreciation": depreciation,
        "amortization": amortization,
        "current_assets": current_assets,
        "liabilities": liabilities,
        "non_cash": non_cash,
        "change_wc": change_wc,
        "capex": capex
    }

    last_result = result
    return redirect(url_for("results"))

   

@app.route("/about")
def about():
    return render_template("about.html")

#Will probably don't need the new analysis since the client can just Edit the metrics in homepage
"""@app.route("/new-analysis")
def new_analysis():

    global last_result
    global last_inputs

    last_result = None
    last_inputs = None

    return redirect(url_for("index"))"""

@app.route("/results")
def results():
    if last_result is None:
        return redirect(url_for("home"))

    return render_template(
        "results.html",
        result=last_result
    )

@app.route("/revenue")
def revenue():

    return render_template(
        "revenue.html",
        result=last_result
    )

@app.route("/details/<metric>")
def metric_details(metric):
    if last_result is None:
        return redirect(url_for("home"))

    details = last_result.get("metric_details", {}).get(metric)
    if details is None:
        return redirect(url_for("results"))

    return render_template("metric_details.html", details=details)

if __name__ == "__main__":
    app.run(debug=True)
