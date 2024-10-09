document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("text-editor-toggle");
    const fileDropdown = document.getElementById("text-editor-dropdown");
    const textArea = document.getElementById("text-editor-textarea");
    
    let saveTimeout;
    const directoryContainer = document.getElementById('document-path');
    const dir = directoryContainer.getAttribute('path');  

    function toggleVisibility() {
        fileDropdown.style.display = fileDropdown.style.display === "flex" ? "none" : "flex";
        textArea.style.display = textArea.style.display === "block" ? "none" : "block";
    }

    toggleBtn.addEventListener("click", toggleVisibility);

    function fetchFiles() {
        console.log("Fetching files from backend...");
        fetch(`/files/?dir=${dir}`)
            .then(response => response.json())
            .then(data => {
                fileDropdown.innerHTML = '';
                data.files.forEach(file => {
                    const option = document.createElement('option');
                    option.value = file;
                    option.textContent = file;
                    fileDropdown.appendChild(option);
                });
            });
    }

    fileDropdown.addEventListener('change', function () {
        console.log("File selected: " + fileDropdown.value);
        fetch(`/file-content/?file=${dir}${fileDropdown.value}`)
            .then(response => response.text())
            .then(data => {
                textArea.value = data;
            });
    });

    textArea.addEventListener('input', function () {
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            const selectedFile = fileDropdown.value;
            const content = textArea.value;

            console.log("Storing content in backend...");
            fetch(`/save-file/?file=${dir}${selectedFile}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: content
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    console.log("File saved successfully");
                    fetch('/reload/');
                    toggleVisibility();
                }
            });
        },5000);
    });

    addEventListener("beforeprint", (event) => {
        fileDropdown.style.display = "none";
        textArea.style.display = "none";
        toggleBtn.style.display = "none";
    });

    addEventListener("afterprint", (event) => {
        toggleBtn.style.display = "block";
    });


    fetchFiles();
});