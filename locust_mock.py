#!/usr/bin/env python
# coding: utf-8

# developer : Nikolai Maksimov (X5 Group)
# date: 17.11.2021

from fastapi import FastAPI
import base64

app = FastAPI()

@app.get("/action_one")
def action_one():
    return 'You did the FIRST action'

@app.get("/action_two")
def action_two():
    return 'You did the SECOND action'

@app.get("/action_three", status_code=302)
def action_three():
    return 'YOU WERE REDIRECTED'

@app.get("/login/{username}")
def token(username: str):
    username_bytes = username.encode('utf-8')
    return base64.standard_b64encode(username_bytes)
