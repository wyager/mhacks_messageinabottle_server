import http
from http import server
PORT = 8005

import bottledb
import coordinates

bdb = bottledb.BottleDB();

with open("log.txt", 'a') as _: # Create the file if it doesn't exist
    pass

with open("log.txt") as state: # Restore to previous state
    for line in state:
        _, ID, lat, lon, data = line.split()
        ID, data = ID.encode(), data.encode()
        lat, lon = float(lat), float(lon)
        bdb.add_bottle(ID, (lat, lon, data))

logfile = open("log.txt",'a')


class CustomHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        #Sample values in self for URL: http://localhost:8080/jsxmlrpc-0.3/
        #self.path  '/jsxmlrpc-0.3/'
        #self.raw_requestline   'GET /jsxmlrpc-0.3/ HTTP/1.1rn'
        #self.client_address    ('127.0.0.1', 3727)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        if self.path.startswith('/get/'):#=='/move':
            ID = self.path[len("/get/"):].encode()
            if ID in bdb.bottles:
                bottle = bdb.bottles[ID]
                lat, lon, data = bottle
                print("/get/ bottle with id {}. Result at lat, lon {}, {}".format(ID.decode(), lat, lon))
                self.wfile.write("{{\"exists\":true, \"lat\":{}, \"lon\":{}, \"data\":\"{}\"}}".format(lat,lon,data.decode()).encode())
            else:
                self.wfile.write(b"{\"exists\": false}")
        elif self.path.startswith('/getat/'):
            print("got getat request")
            lat, lon, radius, *_ = self.path[len('/getat/'):].split('/')
            lat, lon, radius = float(lat), float(lon), float(radius)
            bottles = bdb.spatialdb.get_all(lat, lon)
            bottles = [(ID, bdb.bottles[ID]) for ID in bottles]
            bottles = [(ID, blat, blon, bdata) for (ID, (blat, blon, bdata)) in bottles if coordinates.distance((lat, lon), (blat, blon)) < radius]
            if(len(bottles) > 0):
                ID, lat, lon, data = bottles[0]
                self.wfile.write("[{{\"ID\":\"{}\", \"lat\":{}, \"lon\":{}, \"data\":\"{}\"}}".format(ID.decode(), lat, lon, data.decode()).encode())
                print("/getat/ sending bottle with ID {}. lat, lon {}, {}. Data len is {}.".format(ID.decode(), lat, lon, len(data)))
                for bottle in bottles[1:]:
                    ID, lat, lon, data = bottle
                    self.wfile.write(",{{\"ID\":\"{}\", \"lat\":{}, \"lon\":{}, \"data\":\"{}\"}}".format(ID.decode(), lat, lon, data.decode()).encode())
                    print("/getat/ sending bottle with ID {}. lat, lon {}, {}. Data len is {}.".format(ID.decode(), lat, lon, len(data)))
                self.wfile.write(b"]")
            else:
                self.wfile.write(b"[]")
        elif self.path.startswith('/put/'):
            ID, lat, lon, data, *_ = self.path[len('/put/'):].split('/')
            ID, data = ID.encode(), data.encode()
            lat, lon = float(lat), float(lon)
            print("put request. ID {}, lat,lon {},{}, data len {}".format(ID.decode(), lat, lon, len(data)))
            bdb.add_bottle(ID, (lat, lon, data))
            logfile.write("put {} {} {} {}\n".format(ID.decode(), lat, lon, data.decode()))
            self.wfile.write(b"OK")
        else:
            print("invalid url")
            self.wfile.write(b"Invalid URL")
    def do_POST(self):
        # print(dir(self.headers))
        print("Got POST data")
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)
        items = data.split(b'&')
        items = {i.split(b'=')[0]: i.split(b'=')[1] for i in items}
        ID = items[b'id']
        lat = float(items[b'lat'])
        lon = float(items[b'lng'])
        data = items[b'data']
        print("Got via POST a bottle with ID {}, lat/lon {}, {} and data len {}".format(ID.decode(), lat, lon, len(data)))
        bdb.add_bottle(ID, (lat, lon, data))
        logfile.write("put {} {} {} {}\n".format(ID.decode(), lat, lon, data.decode()))
        print("POST data finished")
        # length = int(self.headers.getheader('content-length'))
        # print(length)
        # data = self.rfile.read(length)
        # print(data)



        

httpd = server.HTTPServer(('', 8005), CustomHandler)
print("serving at port", PORT)
httpd.serve_forever()
logfile.close()
