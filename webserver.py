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
				
			elif self.path.endswith('/restaurants'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				restaurants = session.query(Restaurant).all()
				output = '<html><body>'
				output += "<a href='/restaurants/new'> add a new restaurant </a>"
				output += "</br></br></br>"
				for rest in restaurants:
					output += rest.name
					output += '</br>'
					output += "<a href='/restaurants/%s/edit'>Edit </a>" % str(rest.id)
					output += "</br>"
					output += "<a href='/restaurants/%s/delete'>Delete </a>" % str(rest.id)
					output += "</br></br></br>"
				output += '</body></html>'
				self.wfile.write(output)				
				
			elif self.path.endswith('/restaurants/new'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = '<html><body>'
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Register a new restaurant: </h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
				output += '</html></body>'
				self.wfile.write(output)
				
			elif self.path.endswith('/edit'):
				restId = int(self.path.split('/')[-2])
				rest = session.query(Restaurant).filter_by(id=restId).one()
				if rest:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = '<html><body>'
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><h2>Update restaurant name: </h2><input name='message' type='text' ><input type='submit' value='Update'> </form>" % restId
					output += '</html></body>'
					self.wfile.write(output)
				


		except IOError:
			self.send_error(404, 'File Not Found %s' % self.path)

	def do_POST(self):
		try:
			if self.path.endswith('/restaurants/new'):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')
					newRestaurant = Restaurant(name=messagecontent[0])
					session.add(newRestaurant)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
				
			if self.path.endswith('/edit'):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					restId = self.path.split('/')[-2]
					rest = session.query(Restaurant).filter_by(id=restId).one()
					if rest:
						print('TRUE')
						messagecontent = fields.get('message')
						rest.name = messagecontent
						session.add(rest)
						session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
				


					
						

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