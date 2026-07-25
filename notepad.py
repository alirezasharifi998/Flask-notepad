from app import app, db
from app.models import Subject, Note


@app.shell_context_processor
def shell_context():
    return {"db": db, "Subject": Subject, "Note": Note}
