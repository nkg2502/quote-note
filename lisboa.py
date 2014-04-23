'''
	Lisboa prototype
'''
import os

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
		loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
		extensions = ['jinja2.ext.autoescape'],
		autoescape = True)

class QuoteBook(ndb.Model):
	name = ndb.StringProperty()
	isbn = ndb.StringProperty()
	cover_photo = ndb.BlobKeyProperty()

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

class CreateQuoteBookHandler(webapp2.RequestHandler):

	def get(self):

		page = JINJA_ENVIRONMENT.get_template('createQuoteBook.html')

		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(page.render())

	def post(self):

		name = self.request.get('name')
		isbn = self.request.get('isbn')

		user = users.get_current_user()

		if user:
			quoteBook = QuoteBook(parent=ndb.Key('User', user.email()))
			quoteBook.name = name
			quoteBook.isbn = isbn 
			quoteBook.put()

		self.redirect('/')

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/createQuoteBook', CreateQuoteBookHandler),
], debug=True)

