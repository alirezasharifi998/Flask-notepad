from app import app, db
from app.models import Note, Subject, Folder
from app.components import *
from flask import request, redirect, render_template, flash, url_for


@app.route("/")
@app.route("/index")
def index():
    subjects = list(Subject.query.all())

    return render_template("subject_menu.html", subs=subjects)


@app.route("/subjects/add", methods=["POST"])
def save_sub():
    name = request.form.get("sub-name")
    sub = Subject(name=name)
    try:
        db.session.add(sub)
        db.session.commit()
        sub = Subject.query.filter_by(name=name).first()
        root = root_folder(sub_id=sub.id)
        db.session.add(root)
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for("index"))


@app.route("/subjects/del/<sub_id>")
def del_sub(sub_id):
    try:
        subject = Subject.query.get(sub_id)
        folders = subject.folders
        if folders:
            for folder in folders:
                folder_notes = folder.notes
                # deleteing the notes related to this subject
                for note in folder_notes:
                    db.session.delete(note)
                # deleting the folders
                db.session.delete(folder)
        # deleting the subject itself
        db.session.delete(subject)
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for("index"))


@app.route("/subjects/<sub_id>/0")
def show_sub(sub_id):
    subs = list(Subject.query.all())  # subs is for the subject_menu html
    folders = list(
        db.session.query(Folder)
        .filter(
            Folder.is_subfolder == False,
            Folder.is_root == False,
            Folder.sub_id == int(sub_id),
        )
        .all()
    )
    folders.reverse()
    root = Folder.query.filter_by(is_root=True, sub_id=sub_id).first()
    notes = list(root.notes)
    notes.reverse()
    # NOTE:HERE WE HAVE DO SOMTHING
    return render_template(
        "notes.html",
        subs=subs,
        notes=notes,
        folders=folders,
        selected=int(sub_id),
        folder_id=0,
    )


@app.route("/subject/<sub_id>/<folder_id>")
def show_folder(sub_id, folder_id):
    subs = list(Subject.query.all())  # subs is for the subject_menu html
    folders = list(
        db.session.query(Folder)
        .filter(
            Folder.is_subfolder == True,
            Folder.is_root == False,
            Folder.parent_folder == int(folder_id),
            Folder.sub_id == int(sub_id),
        )
        .all()
    )
    folders.reverse()
    this_folder = Folder.query.get(int(folder_id))
    notes = list(this_folder.notes)
    notes.reverse()
    # print(this_folder.is_subfolder or not this_folder.is_root)
    # NOTE:HERE WE HAVE DO SOMTHING
    return render_template(
        "notes.html",
        subs=subs,
        notes=notes,
        folders=folders,
        selected=int(sub_id),
        folder_id=int(folder_id),
        is_sub=True if this_folder.is_subfolder or not this_folder.is_root else False,
        parent=this_folder.parent_folder,
    )


@app.route("/subjects/<sub_id>/<folder_id>/notes/add", methods=["POST"])
def add_note(sub_id, folder_id):
    title = request.form.get("title")
    text = request.form.get("text")
    root_redirect = True if int(folder_id) == 0 else False
    if int(folder_id) == 0:
        root = Folder.query.filter_by(is_root=True, sub_id=int(sub_id)).first()
        folder_id = root.id
    note = Note(
        title=title, text=text, type=True, pic_addr="NULL", folder_id=int(folder_id)
    )
    try:
        db.session.add(note)
        db.session.commit()

    except Exception as e:
        print(e)
    if root_redirect:
        return redirect(url_for("show_sub", sub_id=int(sub_id)))
    else:
        return redirect(
            url_for("show_folder", sub_id=int(sub_id), folder_id=int(folder_id))
        )


@app.route("/subjects/<sub_id>/<folder_id>/notes/<note_id>/del")
def del_note(sub_id, folder_id, note_id):
    root_redirect = True if int(folder_id) == 0 else False
    if int(folder_id) == 0:
        root = Folder.query.filter_by(is_root=True, sub_id=int(sub_id)).first()
        folder_id = root.id
    note = Note.query.get(int(note_id))
    try:
        # NOTE:we have to check if the note is pic , delete the photo from it's directory too
        db.session.delete(note)
        db.session.commit()

    except Exception as e:
        print(e)
    if root_redirect:
        return redirect(url_for("show_sub", sub_id=int(sub_id)))
    else:
        return redirect(
            url_for("show_folder", sub_id=int(sub_id), folder_id=int(folder_id))
        )


@app.route("/subjects/<sub_id>/<folder_id>/folders/add", methods=["POST"])
def add_folder(sub_id, folder_id):
    root_redirect = True if int(folder_id) == 0 else False
    folder_name = request.form.get("fold-name")
    if int(folder_id) == 0:
        root = Folder.query.filter_by(is_root=True, sub_id=int(sub_id)).first()
        folder_id = root.id
    new_folder = None
    if root_redirect:
        new_folder = main_folder(name=folder_name, sub_id=int(sub_id))
    else:
        new_folder = sub_folder(
            name=folder_name, sub_id=int(sub_id), parent=int(folder_id)
        )
    try:
        # NOTE:we have to check if the note is pic , delete the photo from it's directory too
        db.session.add(new_folder)
        db.session.commit()
    except Exception as e:
        print(e)
    if root_redirect:
        return redirect(url_for("show_sub", sub_id=int(sub_id)))
    else:
        return redirect(
            url_for("show_folder", sub_id=int(sub_id), folder_id=int(folder_id))
        )


@app.route("/subjects/<sub_id>/<folder_id>/notes/<note_id>")
def show_note(sub_id, folder_id, note_id):
    note = Note.query.get(int(note_id))
    text = note.text
    return render_template(
        "show_note.html",
        folder_id=int(folder_id),
        selected=int(sub_id),
        note_id=int(note_id),
        text=text,
    )


@app.route("/subjects/<sub_id>/<folder_id>/folders/del/<fold_del>")
def del_folder(sub_id, folder_id, fold_del):
    root_redirect = True if int(folder_id) == 0 else False
    fold_to_delete = Folder.query.get(int(fold_del))
    notes = fold_to_delete.notes
    try:
        if notes:
            for note in notes:
                db.session.delete(note)
        db.session.delete(fold_to_delete)
        db.session.commit()
    except Exception as e:
        print(e)
    if root_redirect:
        return redirect(url_for("show_sub", sub_id=int(sub_id)))
    else:
        return redirect(
            url_for("show_folder", sub_id=int(sub_id), folder_id=int(folder_id))
        )


@app.route("/subjects/<sub_id>/<folder_id>/notes/<note_id>/edit", methods=["POST"])
def edit_note(sub_id, folder_id, note_id):
    new_text = request.form.get("text")
    if new_text:
        note = Note.query.get(int(note_id))
        note.text = new_text
        db.session.commit()
    return redirect(
        url_for(
            "show_note",
            sub_id=int(sub_id),
            folder_id=int(folder_id),
            note_id=int(note_id),
        )
    )
