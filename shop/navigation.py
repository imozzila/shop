from flask_nav import Nav, register_renderer
from flask_nav.elements import Navbar, Subgroup, View
from shop import app
from dominate import tags
from flask_nav.renderers import Renderer



nav = Nav(app)
@nav.navigation('banner')
def create_navbar():

    home = View('Signup', 'signup')
    login = View('Login', 'login')
    basket = View('Basket', 'shopping_basket')

    return Navbar('test', login, home, basket)
