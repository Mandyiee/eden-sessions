from . import style
from flask import Flask, render_template,session, request, redirect, url_for,jsonify
from style.forms import CodeForm, StyleForm
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer, guess_lexer, get_lexer_by_name, TextLexer
from pygments.styles import get_all_styles
from utils import take_screenshot_from_url
from pygments import lexers
 

import base64

PLACEHOLDER_CODE = "print('HELLO WORLD')"
DEFAULT_STYLE = "monokai"

from app import app

@style.route('/', methods=["GET","POST"])
def index():
    form = CodeForm()
    form.code.data = session.get('code', PLACEHOLDER_CODE)  # I
    
    if form.validate_on_submit():
        session["code"] = form.code.data
       
    
    lines = session.get('code',' ').split("\n")
   
    context = {
        "message": "Paste Your Python Code 🐍",
        "code":  session.get('code'),
        "form": form, 
         "num_lines": len(lines),
        "max_chars": len(max(lines, key=len)),
    }
    return render_template("index.html", **context)

@style.route("/save_code", methods=["POST"])
def save_code():
    session["code"] = request.form.get("code")
    #print('fhhfddd')
    # print(request.form.get("code"))
    return redirect(url_for("style.index"))

@style.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    session["code"] = PLACEHOLDER_CODE
    return redirect(url_for("style.index"))

def detect_language(code):
    try:
        lexer = guess_lexer(code)
        return lexer.name
    except Exception as e:
        return f"Language detection failed: {str(e)}"
    
# @style.route("/style", methods=["GET"])
# def show_style():
#     if session.get("style") is None:
#         session["style"] = DEFAULT_STYLE
#     formatter = HtmlFormatter(style=session["style"])
    
#     context = {
#         "message": "Select Your Style 🎨",
#         "style_definitions": formatter.get_style_defs(),
#         "style_bg_color": formatter.style.background_color,
#         "highlighted_code": highlight(
#             session["code"], Python3Lexer(), formatter
#         ),
#         "current_style" : session.get("style",DEFAULT_STYLE),
#          "all_styles": list(get_all_styles()),
#          "all_lexers" : list(lexers.get_all_lexers())
#     }
#     return render_template("show_style.html", **context)

from pygments.lexers import guess_lexer_for_filename, get_lexer_by_name

@style.route("/style", methods=["GET"])
def show_style():
    if session.get("style") is None:
        session["style"] = DEFAULT_STYLE
    
    code = session.get('code', PLACEHOLDER_CODE)
    try:
        if session.get("lexer") is None:
            lexer = TextLexer()
        else:
            lexer_specification = session.get('lexer')
            lexer = get_lexer_by_name(lexer_specification[0], aliases=lexer_specification[1])
            print(lexer)
    except Exception as e:
        lexer = TextLexer()
        print(e)
    

    formatter = HtmlFormatter(style=session["style"])
    print(highlight(code, lexer, formatter))
    context = {
        "message": "Select Your Style 🎨",
        "style_definitions": formatter.get_style_defs(),
        "style_bg_color": formatter.style.background_color,
        "highlighted_code": highlight(code, lexer, formatter),
        "current_style": session.get("style", DEFAULT_STYLE),
        "current_lang":session.get('lexer','Text'),
        "all_styles": list(get_all_styles()),
        "all_lexers": list(lexers.get_all_lexers()),
        "font":session.get('font',"'Playfair Display', serif")
    }
    
    return render_template("show_style.html", **context)


@style.route("/save_style", methods=["POST"])
def save_style():
    try:
        data = request.get_json()
        style = data.get('style', DEFAULT_STYLE)
        print(data)
        if style is not None:
            session["style"] = style
        if request.form.get("code") is not None:
            session["code"] = request.form.get("code")
        response_data = {'status': 'done'}
        
        return jsonify(response_data)
    except Exception as e:
        if request.form.get("code") is not None:
            session["code"] = request.form.get("code")
        session["style"] = request.form.get("style",DEFAULT_STYLE)
        return redirect(url_for("style.show_style"))
   

@style.route("/save_lexer", methods=["POST"])
def save_lexer():
    data = request.get_json()
    lexer = data.get('lexer', None)
    
    if lexer is not None:
        print(lexer.split(",,"))
        session["lexer"] = lexer.split(",,")
        
    response_data = {'status': 'done'}
    
    return jsonify(response_data)

@style.route("/save_font", methods=["POST"])
def save_font():
    data = request.get_json()
    font = data.get('font', None)
    print(font)
    if font is not None:
        session["font"] = font
        
    response_data = {'status': 'done'}
    
    return jsonify(response_data)
@style.route("/image", methods=["GET"])
def image():
    session_data = {
        "name": app.config["SESSION_COOKIE_NAME"],
        "value": request.cookies.get(app.config["SESSION_COOKIE_NAME"]),
        "url": request.host_url,
    }
    target_url = request.host_url + url_for("style.show_style")
    image_bytes = take_screenshot_from_url(target_url, session_data)
    context = {
        "message": "Done! 🎉",
        "image_b64": base64.b64encode(image_bytes).decode("utf-8"),
    }
    return render_template("image.html", **context)

