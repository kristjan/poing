import os
import time
import cgi
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Poing(db.Model):
	sender = db.StringProperty(multiline=False)
	receiver = db.StringProperty(multiline=False)
	time = db.DateTimeProperty(auto_now_add=False)


class MainHandler(webapp.RequestHandler):
	
	def get(self):
		self.render('index')

	def post(self):
		data = {
			'from': self.request.get('from'),
			'to': self.request.get('to'),
			'time': time.time()
		}
		self.render('poinged', data)

	def render(self, filename, data=None):
		path = os.path.join(os.path.dirname(__file__), filename+'.html')
		self.response.out.write(template.render(path, data or {}))


def main():
  application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
