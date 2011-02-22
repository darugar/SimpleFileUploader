import os
from google.appengine.api import users
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
        self.response.out.write('Ok. <a href="/list">List</a>')

class ListPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.out.write(
                'Hello %s <a href="%s">Sign out</a><br>' % 
                (user.nickname(), users.create_logout_url("/list"))
            )
            if user.email() == 'your_account@gmail.com':
                items = Content.all().order("-date")
                path = os.path.join(os.path.dirname(__file__), 'templates/list.html')
                self.response.out.write(template.render(path, {'items':items}))
        else:
            self.redirect(users.create_login_url(self.request.uri))

class DeletePage(webapp.RequestHandler):
    def get(self, key):
        item = Content.get(key)
        Content.delete(item)
        self.redirect('/list', False)
        
class ShowPage(webapp.RequestHandler):
    def get(self, key):
        item = Content.get(key)
        #self.response.headers['Content-Type'] = 'text/plain'
        #evaluate the extension, txt and log should be text, otherwise octet-stream
        self.response.headers['Content-Type'] = 'application/octet-stream'
        self.response.out.write(item.contents)

class TestPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        template_values = ()
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
    ('/test', TestPage),
    ('/list', ListPage),
    ('/show/(.*)', ShowPage),
    ('/delete/(.*)', DeletePage),
    ('/upload', UploadPage)
], debug=True)

def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
