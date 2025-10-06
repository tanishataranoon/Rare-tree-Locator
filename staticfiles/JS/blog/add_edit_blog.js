// Preview selected image
document.getElementById("id_image").addEventListener("change", function (event) {
    const preview = document.getElementById("preview");
    preview.innerHTML = "";
    const file = event.target.files[0];

    if (file) {
        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.onload = () => URL.revokeObjectURL(img.src);
        preview.appendChild(img);
    }
});

// Handle Preview Button
document.getElementById("previewBtn").addEventListener("click", function () {
    const title = document.getElementById("id_title").value;
    const content = document.getElementById("id_content").value;
    const category = document.getElementById("id_category").value;

    if (!title || !content) {
        alert("Please enter a title and content before previewing.");
        return;
    }

    const previewWindow = window.open("", "_blank", "width=800,height=600,scrollbars=yes");
    previewWindow.document.write(`
        <html>
        <head>
            <title>Preview - ${title}</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; background: #f5f6fa; }
                h1 { color: #2c3e50; }
                h3 { color: #27ae60; }
                .content { margin-top: 20px; white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <h1>${title}</h1>
            ${category ? `<h3>Category: ${category}</h3>` : ""}
            <div class="content">${content}</div>
        </body>
        </html>
    `);
});

