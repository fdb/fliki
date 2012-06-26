from time import time
from glob import glob
from os.path import basename, splitext

from flask import Flask, request, render_template, redirect, url_for
from markdown import markdown

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("hello_form.html")

@app.route('/greet')
def greet():
    name = request.args.get('name', 'Anonymous')
    if len(name.strip()) == 0:
        name = 'Anonymous'
    return render_template("greeting.html", first_name=name)

@app.route('/wiki')
def page_show_home():
    return page_show('home')
    
@app.route('/wiki/<page_name>')
def page_show(page_name):
    text = _read_page(page_name)
    html = _convert_to_html(text)
    return render_template("page_show.html", content=html, page_name=page_name)

@app.route('/wiki/<page_name>/edit', methods=['GET', 'POST'])
def page_edit(page_name):
    if request.method == 'GET':
        text = _read_page(page_name)
        return render_template("page_edit.html", text=text)
    else:
        text = request.form['text']
        _write_page(page_name, text)
        return redirect('/wiki/%s' % page_name)
        
@app.route('/wiki/all')
def page_list():
    pages = _list_pages()
    return render_template("page_list.html", pages=pages)
    
def _page_name_to_filename(page_name):
    return "pages/%s.md" % page_name.lower()
    
def _filename_to_page_name(fname):
    return splitext(basename(fname))[0]

def _read_page(page_name):
    fname = _page_name_to_filename(page_name)
    return open(fname).read()

def _write_page(page_name, text):
    fname = _page_name_to_filename(page_name)
    open(fname, 'w').write(text)
    
def _list_pages():
    return [_filename_to_page_name(fname) for fname in glob('pages/*.md')]

def _convert_to_html(text):
    return markdown(text)

if __name__=='__main__':
    app.run(debug=True)