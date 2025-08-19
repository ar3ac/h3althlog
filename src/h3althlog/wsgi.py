from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from h3althlog.app import app  # app già istanziata

application = DispatcherMiddleware(Flask("root-dummy"), {
    "/h3althlog": app
})
