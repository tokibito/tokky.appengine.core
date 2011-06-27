from google.appengine.ext import db

def get_by_slug(model, slug):
    return model.all().filter('slug = ', slug).get()