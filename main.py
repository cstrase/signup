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
import re
import webapp2
import cgi




form="""
<form method="post">
<label>
    User Name:
    <input type="text" name="username" value="%(username)s" required>
</label>
<div style="color: red">%(error_username)s</div>
<br>
<label>
    Password:
    <input type="password" name="password" value="%(password)s" required>
</label>
<div style="color: red">%(error_password)s</div>
<br>
<label>
    Verify Password:
    <input type="password" name="verify_password" value="%(verify_password)s" required>
</label>
<div style="color: red">%(error_verify)s</div>
<br>
<label>
Email:
    <input type="text" name="email" value="%(email)s" required>
</label>
<div style="color: red">%(error_email)s</div>
<br>
<input type="submit">
</form>
"""
#reg expressions to check for validity of user input
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(user_name):
        return user_name and USER_RE.match(user_name)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(user_password):
        return PASSWORD_RE.match(user_password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(user_email):
        return not user_email or EMAIL_RE.match(user_email)






class MainHandler(webapp2.RequestHandler):
    def form_Writer(self, username="", error_username="", password="", error_password="",  verify_password="", error_verify="", email="", error_email=""):
        self.response.out.write(form % {"username": username,
                                    "password": password,
                                    "verify_password": verify_password,
                                    "email": email,
                                    "error_password": error_password,
                                    "error_username": error_username,
                                    "error_verify": error_verify,
                                    "error_email": error_email})

    def get(self):
        self.form_Writer()

        #variables that store user input
    def post(self):
        have_error = False
        user_name = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify_password')
        user_email = self.request.get('email')
        #variables to check validity
        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""

        if not valid_username(user_name):
                username = user_name
                username_error="Please provide a correct username"
                have_error = True

        if not valid_email(user_email):
                email = user_email
                email_error="Please provide a correct email address"
                have_error = True


        if not valid_password(user_password):
                password = user_password
                password_error= "Provide a valid password"
                have_error = True


        if  user_verify != user_password:
                verify_error="Your passwords did not match"
                have_error = True

        if have_error:
            self.form_Writer(username = user_name, error_username = username_error, error_password = password_error, error_verify = verify_error, email = user_email, error_email = email_error)

        else:
            self.response.write("Great job " + user_name + "!")

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
