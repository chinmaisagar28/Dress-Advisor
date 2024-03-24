document.getElementById('file-input').addEventListener('change', handleFileSelect);
document.getElementById('drop-area').addEventListener('dragover', handleFileDrop);
document.getElementById('drop-area').addEventListener('drop', handleFileDrop);
document.getElementById('upload-btn').addEventListener('click', handleUpload);

function handleFileSelect(event) {
    var file = event.target.files[0];
    displayPreview(file);
    checkFileSize(file);
}

function handleFileDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    // Set the drop effect to 'copy'
    event.dataTransfer.dropEffect = 'copy';
    if (event.type !== 'drop') return;
    // Check if files were dropped
    if (event.dataTransfer.files.length > 0) {
        var file = event.dataTransfer.files[0];
        // Assigning drag file to file input
        document.getElementById('file-input').files = event.dataTransfer.files;
        // Display preview and check file size
        displayPreview(file);
        checkFileSize(file);
    }
}

function displayPreview(file) {
    var reader = new FileReader();
    reader.onload = function (event) {
        var img = document.getElementById('preview-image');
        img.src = event.target.result;
        img.style.display = 'block';
    }
    reader.readAsDataURL(file);
}

function checkFileSize(file) {
    var fileSize = file.size / 1024 / 1024; // in MB

    if (fileSize > 2) {
        showErrorToast('File size exceeds the maximum limit of 2MB.');
        document.getElementById('upload-btn').disabled = true;
        setTimeout(function () {
            document.getElementById('upload-btn').disabled = false;
        }, 4000); // Enable upload button after 4 seconds
    } else {
        document.getElementById('upload-btn').disabled = false;
    }
}

function handleUpload(event) {
    var fileInput = document.getElementById('file-input');
    var file = fileInput.files[0];
    var genderSelect = document.getElementById('gender');
    var occasionSelect = document.getElementById('occasion');

    if (!file) {
        // If no file is selected, show error message
        showErrorToast('Please select a file.');
    } else if (genderSelect.value === 'none' || occasionSelect.value === 'none') {
        // If gender or occasion is not selected, show error message
        showErrorToast('Please select gender and occasion.');
    } else {
        // If a file is selected and gender/occasion are selected, submit the form
        document.getElementById('upload-form').submit();
    }
    event.preventDefault();
}


function showErrorToast(message) {
    console.log('f2')
    const toast = document.getElementById('error-toast');
    toast.textContent = message;
    toast.classList.add('show');
    toast.classList.add('animate__shakeX'); // Add the animate__shakeX class
    setTimeout(() => {
        toast.classList.remove('show');
        toast.classList.remove('animate__shakeX'); // Remove the animate__shakeX class
    }, 4000); // Hide the toast after 4 seconds
}

// function showErrorToast(message) {
//     const toast = document.getElementById('error-toast');
//     const progressBar = document.getElementById('progress-bar');
//     console.log('f1')
//     // Set the message and show the toast
//     toast.textContent = message;
//     toast.classList.add('show');
//     toast.classList.add('animate__shakeX'); // Add the animate__shakeX class
    
//     // Start the progress bar
//     progressBar.style.transition = 'width 4s linear';
//     progressBar.style.width = '100%';
    
//     // Clear any existing timeouts
//     clearTimeout(progressTimeout);
    
//     // Set a timeout to hide the toast and reset the progress bar
//     const progressTimeout = setTimeout(() => {
//         toast.classList.remove('show');
//         toast.classList.remove('animate__shakeX'); // Remove the animate__shakeX class
//         progressBar.style.width = '0';
//     }, 4000); // Hide the toast after 4 seconds
// }

// // Function to pause the progress bar when hovering over the toast
// function pauseProgressBar() {
//     const progressBar = document.getElementById('progress-bar');
//     progressBar.style.transition = 'none';
// }

// // Function to resume the progress bar when hovering out of the toast
// function resumeProgressBar() {
//     const progressBar = document.getElementById('progress-bar');
//     progressBar.style.transition = 'width 4s linear';
//     progressBar.style.width = progressBar.offsetWidth + 'px'; // Resume from the current width
// }


