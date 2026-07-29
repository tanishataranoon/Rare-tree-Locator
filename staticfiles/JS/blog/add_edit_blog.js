document.addEventListener("DOMContentLoaded", function () {
    // 1. Core Elements
    const blogForm = document.getElementById("blogForm");
    const previewBtn = document.getElementById("previewBtn");
    const imageInput = document.getElementById("id_image");
    const previewContainer = document.getElementById("preview");
    const uploadDropzone = document.getElementById("uploadDropzone");
    const uploadInstructions = document.getElementById("uploadInstructions");

    // 2. Live Image Preview Handler
    if (imageInput) {
        imageInput.addEventListener("change", function (event) {
            if (event.target.files && event.target.files[0]) {
                handleImageFile(event.target.files[0]);
            }
        });
    }

    if (uploadDropzone) {
        ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
            uploadDropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });

        uploadDropzone.addEventListener("drop", function (e) {
            const files = e.dataTransfer ? e.dataTransfer.files : null;
            if (files && files.length > 0) {
                if (imageInput) imageInput.files = files;
                handleImageFile(files[0]);
            }
        });
    }

    function handleImageFile(file) {
        if (!file) return;

        let previewImg = document.getElementById("previewImg");
        if (!previewImg && previewContainer) {
            previewImg = document.createElement("img");
            previewImg.id = "previewImg";
            previewContainer.appendChild(previewImg);
        }

        if (previewImg) {
            previewImg.src = URL.createObjectURL(file);
            previewImg.onload = () => URL.revokeObjectURL(previewImg.src);
        }

        if (previewContainer) {
            previewContainer.classList.remove("hidden");
            previewContainer.style.display = "block";
        }
        if (uploadInstructions) {
            uploadInstructions.style.display = "none";
        }
    }

    // 3. Robust Preview Modal Trigger
    if (previewBtn) {
        previewBtn.addEventListener("click", function (e) {
            e.preventDefault(); // Stop form submission!

            // Safely fetch input values with fallbacks
            const titleEl = document.getElementById("id_title");
            const categoryEl = document.getElementById("id_category");
            const videoUrlEl = document.getElementById("id_video_url");
            const contentEl = document.getElementById("id_content");

            const title = titleEl ? titleEl.value.trim() : "";
            const category = categoryEl ? categoryEl.value.trim() : "";
            const videoUrl = videoUrlEl ? videoUrlEl.value.trim() : "";
            const content = contentEl ? contentEl.value.trim() : "";

            // Check for image preview source
            const previewImg = document.getElementById("previewImg");
            let imgSrc = "";
            if (previewImg && previewImg.src && !previewImg.src.endsWith("#")) {
                imgSrc = previewImg.src;
            } else {
                // Fallback to Django form's rendered image tag if present
                const existingImg = previewContainer ? previewContainer.querySelector("img") : null;
                if (existingImg) imgSrc = existingImg.src;
            }

            // Validation
            if (!title || !content) {
                alert("Please fill in the Title and Content before previewing.");
                return;
            }

            // Remove any existing preview modal
            const existingModal = document.getElementById("previewModal");
            if (existingModal) existingModal.remove();

            // Construct Modal
            const embedUrl = getEmbedUrl(videoUrl);

            const modalHtml = `
                <div id="previewModal" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(5px); z-index: 99999; display: flex; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box;">
                    <div style="background: #ffffff; width: 100%; max-width: 800px; max-height: 90vh; border-radius: 16px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); display: flex; flex-direction: column; overflow: hidden; font-family: system-ui, -apple-system, sans-serif;">
                        
                        <!-- Header -->
                        <div style="display: flex; align-items: center; justify-content: space-between; padding: 16px 24px; border-bottom: 1px solid #e5e7eb; background: #f9fafb;">
                            <span style="font-size: 0.9rem; font-weight: 700; color: #2e7d32; background: #e8f5e9; padding: 6px 12px; border-radius: 20px;">
                                Article Preview
                            </span>
                            <button type="button" id="closePreviewBtn" style="background: none; border: none; font-size: 2rem; color: #6b7280; cursor: pointer; line-height: 1;">&times;</button>
                        </div>
                        
                        <!-- Body -->
                        <div style="padding: 28px; overflow-y: auto; flex: 1; text-align: left;">
                            ${category ? `<div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #2e7d32; margin-bottom: 8px;">${escapeHtml(category)}</div>` : ""}
                            
                            <h1 style="font-size: 1.8rem; font-weight: 800; margin: 0 0 20px 0; color: #111827; line-height: 1.3;">${escapeHtml(title)}</h1>
                            
                            ${imgSrc ? `
                                <div style="width: 100%; max-height: 350px; border-radius: 12px; overflow: hidden; margin-bottom: 24px;">
                                    <img src="${imgSrc}" style="width: 100%; height: 100%; object-fit: cover; display: block;" alt="Featured Image">
                                </div>
                            ` : ""}

                            <div style="font-size: 1.05rem; line-height: 1.7; color: #374151; margin-bottom: 24px;">
                                ${formatContent(content)}
                            </div>

                            ${embedUrl ? `
                                <div style="position: relative; padding-bottom: 56.25%; height: 0; border-radius: 12px; overflow: hidden; margin-top: 20px;">
                                    <iframe src="${embedUrl}" style="position: absolute; top:0; left:0; width:100%; height:100%;" frameborder="0" allowfullscreen></iframe>
                                </div>
                            ` : ""}
                        </div>

                        <!-- Footer -->
                        <div style="padding: 16px 24px; border-top: 1px solid #e5e7eb; background: #f9fafb; display: flex; justify-content: flex-end;">
                            <button type="button" id="closePreviewFooterBtn" style="padding: 10px 20px; background: #6b7280; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">Close Preview</button>
                        </div>

                    </div>
                </div>
            `;

            // Append to body
            document.body.insertAdjacentHTML("beforeend", modalHtml);
            document.body.style.overflow = "hidden";

            // Bind Close Events
            const modal = document.getElementById("previewModal");
            const closeBtn = document.getElementById("closePreviewBtn");
            const closeFooterBtn = document.getElementById("closePreviewFooterBtn");

            function closeModal() {
                if (modal) {
                    modal.remove();
                    document.body.style.overflow = "";
                }
            }

            if (closeBtn) closeBtn.addEventListener("click", closeModal);
            if (closeFooterBtn) closeFooterBtn.addEventListener("click", closeModal);
            if (modal) {
                modal.addEventListener("click", function (evt) {
                    if (evt.target === modal) closeModal();
                });
            }
        });
    }

    // Helpers
    function escapeHtml(text) {
        const div = document.createElement("div");
        div.innerText = text;
        return div.innerHTML;
    }

    function formatContent(text) {
        return text
            .split("\n\n")
            .map((p) => `<p style="margin-bottom: 16px;">${escapeHtml(p).replace(/\n/g, "<br>")}</p>`)
            .join("");
    }

    function getEmbedUrl(url) {
        if (!url) return null;
        const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
        const match = url.match(regExp);
        if (match && match[2].length === 11) {
            return `https://www.youtube.com/embed/${match[2]}`;
        }
        return null;
    }
});