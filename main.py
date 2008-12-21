import os
import time
import cgi
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Poing(db.Model):
	poinger = db.StringProperty(multiline=False)
	poingee = db.StringProperty(multiline=False)
	poinged = db.DateTimeProperty(auto_now=True)


class MainHandler(webapp.RequestHandler):
	
	def get(self):
		self.render('index')

	def post(self):
		poinger = self.request.get('from')
		poingee = self.request.get('to')

		poing = Poing.get_or_insert("%s_%s" % (poinger, poingee),
																poinger=poinger, poingee=poingee)
		poing.put()

		data = { 'poing': poing }
		self.render('poinged', data)


	def render(self, filename, data=None):
		path = os.path.join(os.path.dirname(__file__), filename+'.html')
		self.response.out.write(template.render(path, data or {}))


def main():
  application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
