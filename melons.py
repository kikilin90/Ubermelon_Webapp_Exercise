from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2


app = Flask(__name__) # this creates the app.
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/") #this is required to create the app. otherwise, it's not an app. 
def index():
    """This is the 'cover' page of the ubermelon site""" 
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    melons_list = []
    total = 0.0

    for key, value in session["cart"].iteritems():
        melon = model.get_melon_by_id(key)
        melon_info = {
            "name": melon.common_name,
            "price": ("%.2f" % melon.price),
            "qty": value,
            "total": ("%.2f" %(melon.price * value)),

            }

        total += float(melon_info["total"])
        two_deci = ("%.2f" % total)
        melons_list.append(melon_info)

    return render_template("cart.html",
                melons_in_cart = melons_list,
                subtotal = two_deci)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.
    
    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """

    # return "Oops! This needs to be implemented!"


    # melon = model.get_melon_by_id(id)


    session["cart"] = session.get("cart", {})
    session["cart"][str(id)] = session["cart"].get(str(id), 0) + 1
    print session
    flash('Successfully added to cart!')
    return redirect(url_for("shopping_cart"))

@app.route('/logout')
def logout():
    # remove the user's email from the session if it's there
    session['user'].pop('username',None)
    return redirect(url_for('index'))

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""

    session.clear() # to clear up the session

    if request.method == "POST":

        #print request.form

        session['username'] = request.form['user_email']
        session['password'] = request.form['password']
        print session

    email = session['username']

    check_email = model.get_customer_by_email(email)

    print check_email

    if not check_email:
        flash('Sorry, invalid email address / password.')
    else:
        flash('Successfully logged in! Welcome to Ubermelon!')
        return redirect(url_for('list_melons'))

    return render_template("login.html")


















    # input_email = request.form['email']
    # customer_info = model.get_customer_by_email(input_email)

    # email, givenname, surname = customer_info[0], customer_info[1], customer_info[2]

    # print email, givenname, surname
    # return "HI"

    # if not customer_info:
    #     flash("Sorry, invalid email")
    #     return render_template('login.html')
    # else:
    #     session["user"] = email
    #     session["givenname"] = givenname
    #     session["surname"] = surname
    #     print session
    #     flash("You are now logged in!")
    #     return redirect(url_for("list_melons"))



@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    app.run(debug=True) # this runs the app. 
