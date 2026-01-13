// =====================================================
// UPLOAD BOOK
// =====================================================
const uploadForm = document.getElementById("uploadForm");
const statusBox = document.getElementById("status");

if (uploadForm) {
    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(uploadForm);
        statusBox.innerText = "Uploading book...";

        try {
            const response = await fetch("http://localhost:5000/upload", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                statusBox.className = "status success";
                statusBox.innerText = result.message;
                uploadForm.reset();
            } else {
                statusBox.className = "status error";
                statusBox.innerText = result.message;
            }
        } catch {
            statusBox.className = "status error";
            statusBox.innerText = "Cannot connect to backend.";
        }
    });
}

// =====================================================
// TAB HANDLING
// =====================================================
function showTab(tabId) {
    document.querySelectorAll(".tab-content").forEach(div =>
        div.classList.add("hidden")
    );

    document.querySelectorAll(".tab").forEach(btn =>
        btn.classList.remove("active")
    );

    document.getElementById(tabId).classList.remove("hidden");
    event.target.classList.add("active");

    if (tabId === "chat") loadChatBooks();
    if (tabId === "lesson") loadLessonBooks();
}

// =====================================================
// LOAD BOOKS (CHAT)
// =====================================================
async function loadChatBooks() {
    const select = document.getElementById("bookSelect");
    select.innerHTML = "<option>Loading...</option>";

    const res = await fetch("http://localhost:5000/books");
    const data = await res.json();

    select.innerHTML = "<option value=''>-- Select Book --</option>";
    data.books.forEach(book => {
        select.innerHTML += `<option value="${book}">${book}</option>`;
    });
}

// =====================================================
// CHAT REQUEST
// =====================================================
async function sendQuestion() {
    const book = document.getElementById("bookSelect").value;
    const question = document.getElementById("questionInput").value;
    const answerBox = document.getElementById("answerBox");

    if (!book || !question) {
        answerBox.innerText = "Please select a book and enter a question.";
        return;
    }

    answerBox.innerText = "Thinking...";

    const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ book_id: book, question })
    });

    const data = await response.json();
    answerBox.innerText = response.ok ? data.answer : data.message;
}

// =====================================================
// LOAD BOOKS (LESSON PLAN)
// =====================================================
async function loadLessonBooks() {
    const select = document.getElementById("lessonBookSelect");
    select.innerHTML = "<option>Loading...</option>";

    const res = await fetch("http://localhost:5000/books");
    const data = await res.json();

    select.innerHTML = "<option value=''>-- Select Book --</option>";
    data.books.forEach(book => {
        select.innerHTML += `<option value="${book}">${book}</option>`;
    });
}

// =====================================================
// Formating LESSON PLAN
// =====================================================
function renderLessonPlan(text) {
    let html = text;

    // Headings
    html = html.replace(/\*\*(.*?)\*\*/g, "<h4>$1</h4>");

    // Bullet points
    html = html.replace(/\n\* (.*?)/g, "<li>$1</li>");
    html = html.replace(/(<li>.*<\/li>)/gs, "<ul>$1</ul>");

    // Numbered lists
    html = html.replace(/\n\d+\. (.*?)/g, "<li>$1</li>");
    html = html.replace(/(<li>.*<\/li>)/gs, "<ol>$1</ol>");

    // Paragraphs
    html = html.replace(/\n\n/g, "<br><br>");

    return html;
}

// =====================================================
// GENERATE LESSON PLAN
// =====================================================
async function generateLessonPlan() {
    const book = document.getElementById("lessonBookSelect").value;
    const chapterNum = document.getElementById("lessonChapterInput").value;
    const topic = document.getElementById("lessonTopicInput").value;
    const resultDiv = document.getElementById("lessonResult");

    if (!book || !chapterNum || !topic) {
        resultDiv.innerText = "Please fill all fields.";
        return;
    }

    resultDiv.innerText = "Generating lesson plan... This may take a moment.";

    const response = await fetch("http://localhost:5000/lesson-plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            book_id: book,
            chapter: `Chapter ${chapterNum}`,
            topic: topic
        })
    });

    const data = await response.json();

    if (!response.ok) {
        resultDiv.innerText = data.message || "Failed to generate lesson plan.";
        return;
    }

    resultDiv.innerHTML = `
        <h3>Generated Lesson Plan</h3>
        <div class="lesson-plan">
            ${renderLessonPlan(data.lesson_plan)}
        </div>
    `;
}
