#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import webapp2
import assign_jobs

assign_jobs.setup()

#from google.appengine.api import users

bob = 5 

def py_dict_to_js_dict( d ):
    ret_str ="{"
    for key, value in d.items():
        ret_str = "".join( [ret_str, '"%s":"%s",' %( key, value )] )
    ret_str = "".join([ret_str,"'':''}"])
    return ret_str
    
def reverse_py_dict_to_js_dict( d ):
    ret_str ="{"
    for key, value in d.items():
        ret_str = "".join( [ret_str, '"%s":"%s",' %( value, key )] )
    ret_str = "".join([ret_str,"'':''}"])
    return ret_str

nameDictStr = py_dict_to_js_dict( assign_jobs.name_to_num )
numDictStr = py_dict_to_js_dict( assign_jobs.num_to_name )


class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("""
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="stylesheets/main.css">
    </head>
        <body>
        <script> 
            var nameList = %s """ % nameDictStr)
    self.response.out.write("""     
            var numberList = %s """ % numDictStr)
    self.response.out.write("""         
            function namingFunction(p1,p2)
            {
                var x=document.getElementById(p1);
                var y=document.getElementById(p2);
                y.value = nameList[x.value];
            }
            function numberingFunction(p1,p2)
            {
                var x=document.getElementById(p1);
                var y=document.getElementById(p2);
                y.value = numberList[x.value];
            }
        </script>
            <div id="mainheader">
                <h1>Professor Oak</h1>
                <p>Pok&#233;mon Recommender System</p>
            </div>
            <div id="PageWrapper">
            <div id="instructions">
                <h4>Enter in a Pok&#233;mon by number or by name and press Make Recommendation!</h4>
            </div>
            <form action="/recommendations" method="post">
            <div align="center">
                <textarea name="1-number" id="1-number"  rows=1 cols=4 onchange='namingFunction("1-number","1-name")'>#</textarea>
                <textarea name="1-name" id="1-name"  rows=1 cols=16 onchange='numberingFunction("1-name","1-number")'>Name</textarea>
            </div>
            <div align="center">
                <textarea name="2-number" id="2-number" rows="1" cols="4" onchange='namingFunction("2-number","2-name")'>#</textarea>
                <textarea name="2-name" id="2-name" rows="1" cols="16" onchange='numberingFunction("2-name","2-number")'>Name</textarea>
            </div>
            <div align="center">
                <textarea name="3-number" id="3-number" rows="1" cols="4" onchange='namingFunction("3-number","3-name")'>#</textarea>
                <textarea name="3-name" id="3-name" rows="1" cols="16" onchange='numberingFunction("3-name","3-number")'>Name</textarea>
            </div>
            <div align="center">
                <textarea name="4-number" id="4-number" rows="1" cols="4" onchange='namingFunction("4-number","4-name")'>#</textarea>
                <textarea name="4-name" id="4-name" rows="1" cols="16" onchange='numberingFunction("4-name","4-number")'>Name</textarea>
            </div>
            <div align="center">
                <textarea name="5-number" id="5-number" rows="1" cols="4" onchange='namingFunction("5-number","5-name")'>#</textarea>
                <textarea name="5-name" id="5-name" rows="1" cols="16" onchange='numberingFunction("5-name","5-number")'>Name</textarea>
            </div>
            <div align="center">
                <input type="submit" value="Make Recommendation">
            </div>
            </form>
            </div>
            
            <img id="background" src="sprites/pokeball.png">
        </body>
    </html>""")

class Results(webapp2.RequestHandler):
  def post(self):
    self.response.out.write("""
     <html>
    <head>
        <link rel="stylesheet" type="text/css" href="stylesheets/main.css">
    </head>
        <body>
        <div id="resultsheader">
        <h1>Results</h1></div>
        <form action="/" method="link">
            <input id="returnbutton" type="submit" value="Return">
        </form>
        <div id="resultswrapper">
        <p> <font size=5>Your Pok&#233;mon: </font></p> <pre>""")
    pokeNum = {}
    pokeName = {}
    pokeNum[1]= cgi.escape(self.request.get('1-number'))
    pokeName[1] = cgi.escape(self.request.get('1-name'))
    pokeNum[2]= cgi.escape(self.request.get('2-number'))
    pokeName[2] = cgi.escape(self.request.get('2-name'))
    pokeNum[3]= cgi.escape(self.request.get('3-number'))
    pokeName[3] = cgi.escape(self.request.get('3-name'))
    pokeNum[4]= cgi.escape(self.request.get('4-number'))
    pokeName[4] = cgi.escape(self.request.get('4-name'))
    pokeNum[5]= cgi.escape(self.request.get('5-number'))
    pokeName[5] = cgi.escape(self.request.get('5-name'))
    numRequested = 6
    names = []
    for i in xrange(1,6):
	if(pokeNum[i] != "#"):
	    location = "sprites/%s.png" % pokeNum[i]
	    self.response.out.write("""</pre> <div id="yourPoke"> <p><img src="%s" alt="pokeNum"> #%s - %s </p></div> <pre>""" % (location, pokeNum[i], pokeName[i]))
	    numRequested -= 1
	    names.append(pokeName[i])
    self.response.out.write("""</pre><p style="color:#000000;"> <font size=5>Results: </font></p><pre>""")
    results = assign_jobs.make_party(names, 6 )
    count = 0
    for poke in results:
	count+=1
        returnedNum = poke["num"]
        location = "sprites/%s.png" %returnedNum
        name = poke["name"]
        description = poke["description"]
        self.response.out.write("""</pre> <div id="yourPoke"> <p> %s.) <img src="%s" alt="331"> #%s - %s: %s </p><pre>""" % (count,location,returnedNum, name, description))
    self.response.out.write("""</pre>  </div></body>
    </html>""")

import os
import mimetypes
import logging

class SpriteHandler(webapp2.RequestHandler):
    def get(self, path):
        abs_path = os.path.abspath(os.path.join(self.app.config.get('webapp2_static.static_file_path', 'sprites'), path))
	print(abs_path)
        if os.path.isdir(abs_path) or abs_path.find(os.getcwd()) != 0:
            self.response.set_status(403)
            return
        try:
            f = open(abs_path, 'r')
            self.response.headers.add_header('content-type', mimetypes.guess_type(abs_path)[0])
            self.response.out.write(f.read())
            f.close()
        except:
            self.response.set_status(404)

class StylesheetHandler(webapp2.RequestHandler):
    def get(self, path):
        abs_path = os.path.abspath(os.path.join(self.app.config.get('webapp2_static.static_file_path', 'stylesheets'), path))
	print(abs_path)
        if os.path.isdir(abs_path) or abs_path.find(os.getcwd()) != 0:
            self.response.set_status(403)
            return
        try:
            f = open(abs_path, 'r')
            self.response.headers.add_header('content-type', mimetypes.guess_type(abs_path)[0])
            self.response.out.write(f.read())
            f.close()
        except:
            self.response.set_status(404)


app = webapp2.WSGIApplication([('/', MainPage),
                              ('/recommendations', Results),
			      (r'/sprites/(.+)', SpriteHandler),
			      (r'/stylesheets/(.+)', StylesheetHandler)],
                              debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='80')

if __name__ == '__main__':
    main()
