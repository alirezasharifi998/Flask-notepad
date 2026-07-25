from app.models import *


# adding text

# adding pic

# adding root


def root_folder(sub_id: int) -> Folder:
    return Folder(
        name="root",
        sub_id=sub_id,
        is_root=True,
        is_subfolder=False,
        parent_folder=0,
    )


# adding subfolder


def sub_folder(name: str, sub_id: int, parent: int) -> Folder:
    return Folder(
        name=name, sub_id=sub_id, is_root=False, is_subfolder=True, parent_folder=parent
    )


# adding root's folders == main folders


def main_folder(name: str, sub_id: int) -> Folder:
    return Folder(
        name=name,
        sub_id=sub_id,
        is_root=False,
        is_subfolder=False,
        parent_folder=0,
    )
