import os
import time
import cgi
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):
	
	def get(self):
		path = self.view('index')
		self.response.out.write(template.render(path, {}))

	def post(self):
		path = self.view('poinged')
		
		data = {
			'from': self.request.get('from'),
			'to': self.request.get('to'),
			'time': time.time()
		}
		self.response.out.write(template.render(path, data))

	def view(self, filename):
		return os.path.join(os.path.dirname(__file__), 'views', 'main',
												filename+'.html')


def main():
  application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
