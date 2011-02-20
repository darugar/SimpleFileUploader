import os
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class Content(db.Model):
    username = db.StringProperty()
    uid = db.StringProperty()
    filename = db.StringProperty()
    contents = db.BlobProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class UploadPage(webapp.RequestHandler):
    def post(self):
        item = Content(
            username=self.request.get("username"),
            uid     =self.request.get("uid"),
            filename=self.request.get("filename"),
            contents=db.Blob(self.request.get("file"))
        )
        item.put()
        self.response.out.write("OK")

class ListPage(webapp.RequestHandler):
    def get(self):
        items = Content.all().order("-date")
        path = os.path.join(os.path.dirname(__file__), 'templates/list.html')
        self.response.out.write(template.render(path, {'items':items}))

class ShowPage(webapp.RequestHandler):
    def get(self, key):
        item = Content.get(key)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(item.contents)

class TestPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/test', TestPage),
    ('/list', ListPage),
    ('/show/(.*)', ShowPage),
    ('/upload', UploadPage)
], debug=True)

def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
