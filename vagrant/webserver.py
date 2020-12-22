from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith('/hello'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ''
				output += '<html><body>Hello!'
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='text' ><input type='submit' value='Submit'> </form>"
				output += '</body></html>'
				self.wfile.write(output)
				print(output)
				return
			elif self.path.endswith('/restaurants'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				restaurants = session.query(Restaurant).all()
				output = '<html><body>'
				for rest in restaurants:
					output += rest.name
					output += '</br>'
					output += "<a href='#'>Edit </a>"
					output += "</br>"
					output += "<a href='#'>Delete </a>"
					output += "</br></br></br>"
				output += '</body></html>'
				self.wfile.write(output)
				return
			elif self.path.endswith('/restaurants/new'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = '<html><body>'
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants'><h2>Register a new restaurant: </h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
				output += '</html></body>'
				self.wfile.write(output)
		except IOError:
			self.send_error(404, 'File Not Found %s' % self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.end_headers()

			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')
				newRestaurant = Restaurant(name=messagecontent[0])
				session.add(newRestaurant)
				session.commit()
				output = ''
				output += '<html><body>'
				# output += ' <h2> Okay, how about this: </h2>'
				# output += '<h1> %s <h1>' % messagecontent[0]
				# output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='text' ><input type='submit' value='Submit'> </form>"
				output += "<h2> Updated </h2>"
				output += "</br>"
				output += "<a href=/restaurants> Back </a>"
				output += '</body></html>'
				self.wfile.write(output)
		except:
			pass
		

def main():
	try:
		port = 2525
		server = HTTPServer(('127.0.0.1', port), webserverHandler)
		print('Web server running on port %s' % port)
		server.serve_forever()

	except KeyboardInterrupt:
		print('^C entered, stopping web server')
		server.socket.close()


if __name__ == '__main__':
	main()