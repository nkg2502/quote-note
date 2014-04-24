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

class Quote(ndb.Model):
	content = ndb.StringProperty()
	link = ndb.StringProperty()
	private = ndb.BooleanProperty()

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

class WriteQuoteHandler(webapp2.RequestHandler):

	def get(self):

		user = users.get_current_user()

		if not user:
			self.redirect('/')

		quoteBookListQuery = QuoteBook.query(ancestor=ndb.Key('User', user.email()))
		quoteBookList = quoteBookListQuery.fetch()

		page_value = {
				'book_list': quoteBookList
		}

		page = JINJA_ENVIRONMENT.get_template('writeQuote.html')

		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(page.render(page_value))

	def post(self):
		msg = self.request.get('msg')
		book_id = self.request.get('book_id')
		link = self.request.get('link')
		private = self.request.get('private')

		user = users.get_current_user()

		if user:
			quote = Quote(parent=ndb.Key('User', user.email(), QuoteBook, int(book_id)))
			quote.content = msg
			quote.link = link
			quote.private = private == 'True'
			quote.put()

		self.redirect('/')

class ReadQuoteHandler(webapp2.RequestHandler):

	def get(self):

		quoteQuery = Quote.query()
		rawQuoteList = quoteQuery.fetch()
		
		quoteList = []
		for quote in rawQuoteList:
			if not quote.private:
				quoteList.append({
					'user' : quote.key.parent().get().key.parent().string_id(),
					'book_name': quote.key.parent().get().name,
					'content' : quote.content,
					'link' : quote.link
				})

		page_value = {
				'quote_list': quoteList
		}

		page = JINJA_ENVIRONMENT.get_template('readAllQuote.html')

		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(page.render(page_value))

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/createQuoteBook', CreateQuoteBookHandler),
	('/writeQuote', WriteQuoteHandler),
	('/displayQuote', ReadQuoteHandler),
], debug=True)

