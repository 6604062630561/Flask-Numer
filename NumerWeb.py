from flask import Flask, request, render_template_string
from sympy import sympify, Symbol
from math import inf

app = Flask(__name__)

def bisection_method(fx, xl, xr, epsilon):
    x = Symbol("x")
    xm = (xl + xr) / 2
    fxm = fx.subs(x, xm)
    fxr = fx.subs(x, xr)
    if fxm * fxr < 0:
        xl = xm
    else:
        xr = xm

    iterations = []
    i = 0
    criterion = inf

    while criterion > epsilon:
        xmnew = (xl + xr) / 2
        fxm = fx.subs(x, xmnew)
        fxr = fx.subs(x, xr)

        if fxm * fxr < 0:
            xl = xmnew
        else:
            xr = xmnew

        criterion = abs((xmnew - xm) / xmnew)
        iterations.append(f"Iteration {i+1}: xm = {xmnew}, criterion = {criterion}")

        xm = xmnew
        i += 1

    # return all iterations + summary
    summary = {
        "iterations": i,
        "result": xm,
        "log": iterations
    }
    return summary


# 🔹 HTML Page
HTML = """
<!DOCTYPE html>
<html>
  <head>
    <title>Bisection Method</title>
  </head>
  <body>
    <h2>Bisection Calculator</h2>
    <form method="post">
      f(x): <input type="text" name="fx" placeholder="e.g. x**4 - 13"><br><br>
      Left (xl): <input type="text" name="xl"><br><br>
      Right (xr): <input type="text" name="xr"><br><br>
      Epsilon: <input type="text" name="epsilon"><br><br>
      <input type="submit" value="Compute">
    </form>
    {% if summary %}
      <h3>Iterations</h3>
      <pre>
{% for line in summary.log %}
{{ line }}
{% endfor %}
      </pre>
      <h3>Summary</h3>
      Iteration number: {{ summary.iterations }}<br>
      x = {{ summary.result }}
    {% endif %}
  </body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    if request.method == "POST":
        fx_input = request.form["fx"]
        xl = float(request.form["xl"])
        xr = float(request.form["xr"])
        epsilon = float(request.form["epsilon"])

        fx = sympify(fx_input)
        summary = bisection_method(fx, xl, xr, epsilon)

    return render_template_string(HTML, summary=summary)


if __name__ == "__main__":
    app.run(debug=True)
