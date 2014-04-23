'''
	Lisboa prototype
'''
import os

from google.appengine.api import users

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
		loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
		extensions = ['jinja2.ext.autoescape'],
		autoescape = True)

class MainPage(webapp2.RequestHandler):

	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

		user = users.get_current_user()

		nickname = ''
		log_url = users.create_login_url(self.request.uri)
		log_msg = 'Login'

		if user:
			nickname = user.nickname()
			log_url = users.create_logout_url(self.request.uri)
			log_msg = 'Logout'

		index_page_value = {
				'nickname': nickname,
				'log_url': log_url,
				'log_msg': log_msg
		}

		index_page = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(index_page.render(index_page_value))

application = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)

