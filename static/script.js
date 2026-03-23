let mode = "calories";
let selectedDate = "";
let isEditing = false;

document.addEventListener('DOMContentLoaded', function () {

    let calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
        initialView: 'dayGridMonth',

        dateClick: function (info) {
            selectedDate = info.dateStr;

            document.getElementById("selectedDateText").innerText =
                "Selected Date: " + formatDate(selectedDate);

            loadNotes();
        }
    });

    calendar.render();

    // Auto expand textarea
    let textarea = document.getElementById("noteInput");
    textarea.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
    });
});

function setMode(selectedMode) {
    mode = selectedMode;

    document.getElementById("currentMode").innerText =
        mode === "calories" ? "Calories Counter" : "Exercise Tracker";

    document.getElementById("calBtn").classList.toggle("active", mode === "calories");
    document.getElementById("exBtn").classList.toggle("active", mode === "exercise");

    loadNotes();
}

function saveNote() {
    let content = document.getElementById("noteInput").value;

    if (!selectedDate) {
        alert("Select date first!");
        return;
    }

    fetch('/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ date: selectedDate, type: mode, content })
    })
    .then(() => {
        document.getElementById("noteInput").value = "";
        isEditing = false;
        document.getElementById("saveBtn").innerText = "Save";
        loadNotes();
    });
}

function loadNotes() {
    if (!selectedDate) return;

    fetch(`/get/${selectedDate}/${mode}`)
    .then(res => res.json())
    .then(data => {

        let list = document.getElementById("notesList");
        list.innerHTML = "";

        if (data.length > 0) {
            let note = data[0]; // only one note

            // Show note
            list.innerHTML = `
                <div class="note-card">
                    <p>${note.content}</p>
                    <button onclick="editNote(\`${note.content}\`)">Edit</button>
                    <button onclick="deleteNote(${note.id})">Delete</button>
                </div>
            `;

            // Put content in textbox (edit mode)
            document.getElementById("noteInput").value = note.content;
            isEditing = true;
            document.getElementById("saveBtn").innerText = "Update";

        } else {
            document.getElementById("noteInput").value = "";
            isEditing = false;
            document.getElementById("saveBtn").innerText = "Save";
        }
    });
}

function editNote(content) {
    document.getElementById("noteInput").value = content;
    isEditing = true;
    document.getElementById("saveBtn").innerText = "Update";
}

function deleteNote(id) {
    fetch(`/delete/${id}`, { method: 'DELETE' })
        .then(() => {
            document.getElementById("noteInput").value = "";
            document.getElementById("saveBtn").innerText = "Save";
            loadNotes();
        });
}

// ✅ Date format dd-mm-yyyy
function formatDate(dateStr) {
    let d = new Date(dateStr);
    let day = String(d.getDate()).padStart(2, '0');
    let month = String(d.getMonth() + 1).padStart(2, '0');
    let year = d.getFullYear();
    return `${day}-${month}-${year}`;
}