import openai
import sqlite3
from .config import Config
import json
from uuid import uuid4
from flask import Blueprint, render_template, request, redirect, url_for, current_app

openai.api_key = Config.OPENAI_APIKEY


messages_cache = {}
responses_cache = {}


def ask_chatgpt(question, data, chat_id=str(uuid4())):
    if data is None:
        print("NO DATA RECEIVED")
        return {"id": chat_id, "role": "system", "content": "Data not found"}

    try:
        messages = [
            {
                "role": "system",
                "content": f"""
                    You are a helpful assistant. 
                    You have access to the following data: {json.dumps(data)}. 
                    If you don't have information regarding something, you will say so.
                    Use the product name and manufacturer name and then look at the ingredients list.
                    You have the liberty to provide an opinion on manufacturers with the supplier_rating parameter.
                    Output in simple and short text unless longer text is absolutely required.
                    """,
            },
            {"role": "user", "content": question},
        ]

        if chat_id in messages_cache:
            messages = messages_cache[chat_id] + messages
        else:
            messages_cache[chat_id] = []

        print("ASKING CHATGPT")
        print(messages)

        if json.dumps(messages) in responses_cache:
            response = responses_cache[json.dumps(messages)]
        else:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                # prompt=json.dumps(messages),
                messages=messages,
            )
        res = {
            "id": chat_id,
            "role": "system",
            "content": response.choices[0].message.content,
        }
        inp = {"id": chat_id, "role": "user", "content": question}

        responses_cache[json.dumps(messages)] = response
        messages_cache[chat_id].extend([inp, res])

        print("RECEIVED RES")
        print(response)
        print(messages_cache[chat_id])

        return res

    except Exception as e:
        print("EXCEPTION:")
        print(e)
        return {
            "id": chat_id,
            "role": "system",
            "content": "Sorry, I couldn't get a response at the moment.",
        }


chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/<product_id>/<chat_id>", methods=["GET", "POST"])
def chat(product_id, chat_id):
    db_instance = current_app.config["DB_INSTANCE"]
    # If chat_id doesn't exist, generate a new one and redirect
    if chat_id == "new":
        chat_id = str(uuid4())
        return redirect(url_for("chat.chat", product_id=product_id, chat_id=chat_id))

    if request.method == "POST":
        print("POST RECEIVeD")
        # Retrieve the message from the form and store it
        user_message = request.form.get("message")
        if user_message:
            print("USER MESSAGE RECEIVED:", user_message)
            data = db_instance.getFullProduct(product_id)
            print("DATA:", data)
            ask_chatgpt(user_message, data, chat_id)

        return redirect(url_for("chat.chat", product_id=product_id, chat_id=chat_id))

    print(messages_cache)

    if chat_id not in messages_cache:
        messages_cache[chat_id] = []

    # Retrieve chat messages for this session
    chat_history = messages_cache[chat_id]
    prod = db_instance.getFullProduct(product_id)

    return render_template(
        "chat.jinja",
        product=prod,
        product_id=product_id,
        chat_id=chat_id,
        chat_history=chat_history,
    )
