import os
import time
import cgi
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

MISSING_DATA = "You must specify both a poinger and a poingee."

class Poing(db.Model):
	poinger = db.StringProperty()
	poingee = db.StringProperty()
	poinged = db.DateTimeProperty(auto_now=True)

class SmartHandler(webapp.RequestHandler):
	def render(self, filename, data=None):
		path = os.path.join(os.path.dirname(__file__), filename+'.html')
		self.response.out.write(template.render(path, data or {}))


class MainHandler(SmartHandler):
	def get(self):
		self.render('index', {'msg': self.request.get('msg')})


class PoingHandler(SmartHandler):
	def get(self):
		poinger = self.request.get('poinger')
		poingee = self.request.get('poingee')
		if not poinger or not poingee:
			self.redirect('/?msg=%s' % MISSING_DATA)
			return
		poinger = poinger.lower()
		poingee = poingee.lower()

		poing = Poing.get_by_key_name("%s_%s" % (poinger, poingee))
		poing = poing or Poing(poinger=poinger, poingee=poingee)

		data = { 'poing': poing }
		self.render('poing', data)

	def post(self):
		poinger = self.request.get('poinger')
		poingee = self.request.get('poingee')
		if not poinger or not poingee:
			self.redirect('/?msg=%s' % MISSING_DATA)
			return
		poinger = poinger.lower()
		poingee = poingee.lower()

		poing = Poing.get_or_insert("%s_%s" % (poinger, poingee),
																poinger=poinger, poingee=poingee)
		poing.put()
		poing = Poing.get(poing.key()) # Reload timestamp from put()

		data = { 'poing': poing }
		self.render('poing', data)


def main():
  application = webapp.WSGIApplication([('/', MainHandler),
																				('/poing', PoingHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
