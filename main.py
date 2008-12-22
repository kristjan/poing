import os
from datetime import datetime
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
		self.response.content_type = 'text/plain'
		poinger = self.request.get('poinger')
		poingee = self.request.get('poingee')
		if not poinger or not poingee:
			self.response.out.write('ERROR')
			return
		poinger = poinger.lower()
		poingee = poingee.lower()

		poing = Poing.get_by_key_name("%s_%s" % (poinger, poingee))

		now = datetime.utcnow()
		if poing:
			poinged = poing.poinged
		else:
			poinged = now
		time_since_poing = time_in_seconds(now - poinged)
		
		self.response.content_type = 'text/plain'
		self.response.out.write(time_since_poing)

	def post(self):
		self.response.content_type = 'text/plain'
		poinger = self.request.get('poinger')
		poingee = self.request.get('poingee')
		if not poinger or not poingee:
			self.response.out.write('ERROR')
			return
		poinger = poinger.lower()
		poingee = poingee.lower()

		poing = Poing.get_or_insert("%s_%s" % (poinger, poingee),
																poinger=poinger, poingee=poingee)
		poing.put() # Updates poinged

		self.response.out.write('OK')

DAYS_TO_SECONDS = 24*60*60
def time_in_seconds(delta):
	return delta.days * DAYS_TO_SECONDS + delta.seconds

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
																				('/poing', PoingHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
