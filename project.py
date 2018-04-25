# Import Framework Flask
from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify

# Import SQLAlchemy toolkit object-relational mapper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import Database
from database_setup import Base, Restaurant, MenuItem

# Start Flask
app = Flask(__name__)

# Create DB engine
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

# Create Session
DBSession = sessionmaker(bind=engine)
session = DBSession()


#JSON
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id,
        id=menu_id).one()
    return jsonify(MenuItems=[item.serialize])
# JSON ENDPoint


# Main Page & Hello Page
@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurant = session.query(Restaurant).first()
    return redirect(url_for('restaurantMenu', restaurant_id=
        restaurant.id))

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id=
            restaurant_id)
        session.add(newItem)
        session.commit()
        flash('New menu item created')
        return redirect(url_for('restaurantMenu', restaurant_id=
            restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=
            restaurant_id)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:

        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id,
             item=editedItem)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',
            methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash('Menu item has been deleted')
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template(
            'deletemenuitem.html', restaurant_id=restaurant_id, menu_id=
                menu_id, item=deletedItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
