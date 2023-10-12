document.addEventListener('DOMContentLoaded', function() {
    var fileTypeSelect = document.getElementById("file_type");
    var fileInput = document.getElementById("file");
    var convertToHyperBtn = document.querySelector('button[value=".hyper"]');
    var convertToCsvBtn = document.querySelector('button[value=".csv"]');

    function updateButtonStates() {
        if (fileTypeSelect.value === ".csv") {
            convertToHyperBtn.disabled = false; 
            convertToCsvBtn.disabled = true;
        } else {
            convertToHyperBtn.disabled = false;
            convertToCsvBtn.disabled = false;
        }
    }

    function updateFileTypes() {
        var selectedFileType = fileTypeSelect.value;
        var allowedFileTypes = {
            '.RDS': 'application/rds',
            '.txt': 'text/plain',
            '.sav': 'application/x-spss-sav',
            '.csv': 'text/csv',
        };

        fileInput.removeAttribute('accept');

        if (allowedFileTypes[selectedFileType]) {
            fileInput.setAttribute('accept', allowedFileTypes[selectedFileType]);
        }
    }

    updateButtonStates();
    updateFileTypes();

    fileTypeSelect.addEventListener('change', function() {
        updateButtonStates();
        updateFileTypes();
    });
});