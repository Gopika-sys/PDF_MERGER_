document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('pdf-files');
    const fileCount = document.getElementById('file-count');
    
    fileInput.addEventListener('change', function() {
        const numFiles = fileInput.files.length;
        if (numFiles > 0) {
            fileCount.textContent = `${numFiles} file(s) selected`;
        } else {
            fileCount.textContent = '';
        }
    });
});
