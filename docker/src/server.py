import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from sklearn.neighbors import KNeighborsClassifier

with open('convert.txt') as json_file:
    url_to_embedding = json.load(json_file)

    values = list(url_to_embedding.values())
    url_outputs = list(url_to_embedding.keys())
    del url_to_embedding

    neigh = KNeighborsClassifier(n_neighbors=10)
    neigh.fit(values, url_outputs)

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def url_to_images(self, url):
        url = str(url)
        for i in range(3):
            url = url[url.find('/')+1:]    # get rid of the first 3 / in the website to get just the request
        url = "-" + url.replace('/', '-')   # remove the rest of the / and replace them for -
        url = url[0:-1]   # trim the last string for input
        distances, indexes = neigh.kneighbors([values[url_outputs.index(url)]], 10) # get 10 nearest neighbors
        urls_to_return = []
        for x in indexes[0]:
            urls_to_return.append(url_outputs[x])
        return urls_to_return    # 2d array is returned

    def image_to_url(self, image): # takes in the image data stored in the json and turns it into a valid url
        return 'https://www.valentino.com' + image.replace('-','/')

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        self.send_response(200) # just assume that it was a valid request
        self.send_header("Content-type", "application/json")
        self.end_headers()

        image_dict = {}
        for i, image in enumerate(self.url_to_images(post_data)):
            image_dict[i] = self.image_to_url(image)

        json_str = json.dumps(image_dict)
        self.wfile.write(bytes(json_str, "utf-8"))

def run(server_class=HTTPServer, handler_class=S):
    """Entrypoint for python server"""
    print("running")
    server_address = ("0.0.0.0", 8000)
    httpd = server_class(server_address, handler_class)
    print("launching server...")
    httpd.serve_forever()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
