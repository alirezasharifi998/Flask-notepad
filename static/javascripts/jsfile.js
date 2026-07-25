function add_subject() {
    var box = document.getElementById("sub-input-box");
    box.style.display = 'inline-block';
}

function unselect_sub() {
    var selected = document.getElementById("selected-sub");
    if (selected) {
        selected.id = "";
        selected.className = "";
    }
}
function select_sub(sub) {
    if (sub.id == "selected-sub") {
        window.location.assign("/index");
        return;
    }
    unselect_sub();
    // sub.id = "selected-sub";
    // sub.className = "is-active"
    window.location.assign(sub.getAttribute("data-href"))
}

function del_subject() {
    var selected = document.getElementById("selected-sub");
    window.location.assign(selected.getAttribute('data-del'))
}

function add_note() {
    var title = document.getElementById("input-title");
    var text = document.getElementById("input-textarea");

    if (!title.value) {
        alert("title is empty!");
        return;
    }
    if (!text.value) {
        alert("text is empty");
        return;
    }
    document.getElementById("input-form").submit();
}

function unselect_node() {
    var selected = document.getElementById("selected-node");
    if (selected) {
        selected.id = "";
        selected.className = "panel-block";
    }
}

function select_node(note_fold) {
    if (note_fold.id == "selected-node") {
        unselect_node();
        return;
    }
    unselect_node();
    note_fold.id = "selected-node";
    note_fold.className += " is-active has-background-grey-light";
}


function del_node() {
    var selected = document.getElementById("selected-node");
    window.location.assign(selected.getAttribute("data-del"));
}

function add_folder() {

    var input = document.getElementById("fold-input-box");
    input.style.display = "inline-block"
}

function show_node(note) {
    window.location.assign(note.getAttribute("data-show"));
}
function back_page(btn) {
    window.location.assign(btn.getAttribute("data-lastpage"))
}

function edit_note() {
    var edit_btn = document.getElementById("edit-note-btn");
    var other_btns = document.getElementById("show-btns");
    edit_btn.style.display = "none";
    other_btns.style.display = "inline-block";
    var textbox = document.getElementById("show-note-textarea");
    textbox.readOnly = false;
    var ltrBtn = document.getElementById("ltr-note-btn");
    var rtlBtn = document.getElementById("rtl-note-btn");
    ltrBtn.style.display = rtlBtn.style.display = "none";
}

function ltr() {
    var text = document.getElementById("show-note-textarea");
    text.style.textAlign = "left";
    text.dir = "ltr";
    var ltrBtn = document.getElementById("ltr-note-btn");
    var rtlBtn = document.getElementById("rtl-note-btn");
    ltrBtn.style.display = "none";
    rtlBtn.style.display = "inline-block";
}
function rtl() {
    var text = document.getElementById("show-note-textarea");
    text.style.textAlign = "right";
    text.dir = "rtl";
    var ltrBtn = document.getElementById("ltr-note-btn");
    var rtlBtn = document.getElementById("rtl-note-btn");
    rtlBtn.style.display = "none";
    ltrBtn.style.display = "inline-block";
}