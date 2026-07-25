from app import db
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import Relationship


class Subject(db.Model):
    id = Column(Integer, index=True, primary_key=True)
    name = Column(String(200), index=True, unique=True)
    folders = Relationship("Folder", backref="subject", lazy="dynamic")

    def __repr__(self):
        return "<Subject('{}') , id : {}>".format(self.name, self.id)


class Folder(db.Model):
    id = Column(Integer, index=True, primary_key=True)
    name = Column(String(200), index=True)
    sub_id = Column(Integer, ForeignKey("subject.id"))
    notes = Relationship("Note", backref="folder", lazy="dynamic")
    is_subfolder = Column(Boolean)
    is_root = Column(Boolean)
    parent_folder = Column(Integer)

    def __repr__(self) -> str:
        return "<Folder('{}'), id : {} , sub : {} , root : {} , parent : {} >".format(
            self.name,
            self.id,
            self.sub_id,
            self.is_root,
            self.parent_folder if self.is_subfolder else "NULL",
        )


class Note(db.Model):
    id = Column(Integer, index=True, primary_key=True)
    title = Column(String(250))
    type = Column(Boolean)
    text = Column(Text)
    pic_addr = Column(String(250))
    folder_id = Column(Integer, ForeignKey("folder.id"))

    def __repr__(self) -> str:
        return "<Note('{}') , id : {} , folder : {} , type : {} >".format(
            self.title, self.id, self.folder_id, "text" if self.type else "pic"
        )
