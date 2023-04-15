from flask import Flask, render_template, request

# Constants
# Surcharge tip percent
expected_tip_percent = 0.20

# A typical tip out would be roughly 3% of the total sales
food_tip_rate = 0.03
bar_tip_rate = 0.04
overall_tip_rate = 0.02
host_tip_rate = 0.01


# Helper Functions
def weighted_final_tip(tip_rate, sales, tips_taken_ratio):
    pre_tip_amt = tip_rate * sales

    weighted_final_tip = tips_taken_ratio * pre_tip_amt

    return weighted_final_tip


def currency_format(amount):
    formatted = "${:,.2f}".format(float(amount))
    return formatted


def percent_format(decimal):
    formatted = "{0:0.1%}".format(float(decimal))
    return formatted


Flask_App = Flask(__name__, static_folder="./static", template_folder="./templates")


@Flask_App.route("/", methods=["GET"])
def index():
    """Displays the index page accessible at '/'"""

    return render_template("index.html")


@Flask_App.route("/more_info/", methods=["GET"])
def more_info():
    """Displays Background Information Page"""

    content = {
        "food_tip_rate": percent_format(food_tip_rate),
        "bar_tip_rate": percent_format(bar_tip_rate),
        "overall_tip_rate": percent_format(overall_tip_rate),
        "host_tip_rate": percent_format(host_tip_rate),
    }

    return render_template("more_info.html", **content)


@Flask_App.route("/operation_result/", methods=["POST"])
def operation_result():
    """Route where we send calculator form input"""

    # Take Inputs from Server

    # Sales
    bottle_beer = float(request.form["Input0"] or 0)
    draft_beer = float(request.form["Input1"] or 0)
    food = float(request.form["Input2"] or 0)
    liquor = float(request.form["Input3"] or 0)
    na_bev = float(request.form["Input4"] or 0)
    wine = float(request.form["Input5"] or 0)
    wine_bottle = float(request.form["Input6"] or 0)

    # Combined Bar Sales
    bar = bottle_beer + draft_beer + liquor + na_bev + wine + wine_bottle
    adj_bar = bottle_beer + draft_beer + liquor + na_bev + wine

    # Tips
    card_tips = float(request.form["Input7"] or 0)
    cash_tips = float(request.form["Input8"] or 0)
    total_tips = card_tips + cash_tips

    try:
        # Prepare Numbers
        overall_sales = food + adj_bar
        expected_tip_amount = expected_tip_percent * overall_sales

        # Caculate Tips Taken Ratio
        tips_taken_ratio = round(total_tips / expected_tip_amount, 4)

        # Calculate Final Tip Out Amounts
        final_tip_out_food = weighted_final_tip(food_tip_rate, food, tips_taken_ratio)
        final_tip_out_bar = weighted_final_tip(bar_tip_rate, adj_bar, tips_taken_ratio)
        final_tip_out_overall = weighted_final_tip(
            overall_tip_rate, overall_sales, tips_taken_ratio
        )
        final_tip_out_host = weighted_final_tip(
            host_tip_rate, overall_sales, tips_taken_ratio
        )
        total_tip_out = (
            final_tip_out_host
            + final_tip_out_overall
            + final_tip_out_food
            + final_tip_out_bar
        )

        # Calculate Total Walking Amount
        walking_with = float(total_tips) - float(total_tip_out)

        calculation_success = True

        # Create output
        content = {
            "bottle_beer": currency_format(bottle_beer),
            "draft_beer": currency_format(draft_beer),
            "food": currency_format(food),
            "liquor": currency_format(liquor),
            "na_bev": currency_format(na_bev),
            "wine": currency_format(wine),
            "wine_bottle": currency_format(wine_bottle),
            "card_tips": currency_format(card_tips),
            "cash_tips": currency_format(cash_tips),
            "food_tip_rate": percent_format(food_tip_rate),
            "bar_tip_rate": percent_format(bar_tip_rate),
            "overall_tip_rate": percent_format(overall_tip_rate),
            "total_food_sales": currency_format(food),
            "total_bar_sales": currency_format(adj_bar),
            "total_wine_bottle_sales": currency_format(wine_bottle),
            "overall_sales": currency_format(overall_sales),
            "total_tips": currency_format(total_tips),
            "expected_tip_amount": currency_format(expected_tip_amount),
            "tips_taken_ratio": percent_format(tips_taken_ratio),
            "final_tip_out_food": currency_format(final_tip_out_food),
            "final_tip_out_bar": currency_format(final_tip_out_bar),
            "final_tip_out_overall": currency_format(final_tip_out_overall),
            "final_tip_out_host": currency_format(final_tip_out_host),
            "total_tip_out": currency_format(total_tip_out),
            "walking_with": currency_format(walking_with),
            "calculation_success": calculation_success,
        }

        # Display all values on screen
        return render_template("results.html", **content)

    except ZeroDivisionError:
        content = {
            "error": "Cannot perform calculation with provided input.",
            "calculation_success": False,
            "result": "Bad Input",
        }

        return render_template("results.html", **content)

    except ValueError:
        content = {
            "error": "Cannot perform calculation with provided input.",
            "calculation_success": False,
            "result": "Bad Input",
        }

        return render_template("results.html", **content)


if __name__ == "__main__":
    Flask_App.debug = True
    Flask_App.run()
