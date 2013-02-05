import os
import re
import jinja2
import webapp2
from jinja2 import evalcontextfilter, Markup, escape, Environment,\
    FileSystemLoader
from utils.converter import csv2dict

@evalcontextfilter
def linebreaks(eval_ctx, value):
    """Converts newlines into <p> and <br />s."""
    value = re.sub(r'\r\n|\r|\n', '\n', value) # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'<p>%s</p>' % p.replace('\n', '<br />') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)
 
@evalcontextfilter
def linebreaksbr(eval_ctx, value):
    """Converts newlines into <p> and <br />s."""
    value = re.sub(r'\r\n|\r|\n', '\n', value) # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'%s' % p.replace('\n', '<br />') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)

PROJECT_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
env.filters['linebreaks'] = linebreaks
env.filters['linebreaksbr'] = linebreaksbr


def reduce_word(text):
    """Using Reduce Functional Style"""
    dictionary = csv2dict()
    dictionary.update(csv2dict('data2.csv'))
    return reduce(lambda t, kv: t.replace(*kv), dictionary.iteritems(), text)

def replace_redundancy(text):
    dictionary = csv2dict()
    for i, j in dictionary.iteritems():
        text = text.replace(i, j)
    return text


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('index.html')
        self.response.write(template.render())

    def post(self):
        template = env.get_template('index.html')
        text = self.request.get('text')
        shorten = reduce_word(text)
        word_reduce_count = len(text.split()) - len(shorten.split())
        self.response.write(template.render(text=text, shorten=shorten,
            word_reduce_count=word_reduce_count))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ], debug=True)
