let destinationPath = null;

// 1. Select destination folder
async function selectDestination() {
  try {
    // Prompt for folder path
    const folderPath = prompt('Enter destination folder path:\n(e.g., C:\\Users\\YourName\\Pictures)');
    
    if (!folderPath) return;
    
    const response = await fetch('/api/select-destination', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: folderPath })
    });
    
    const data = await response.json();
    
    if (data.success) {
      destinationPath = data.path;
      document.getElementById("step1").classList.add("hidden");
      document.getElementById("step2").classList.remove("hidden");
      log(`✅ Destination set: ${data.name}`);
    } else {
      alert(`Error: ${data.error}`);
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
}

// 2. Listen for file selection and transfer
document.getElementById("sourceInput").addEventListener("change", async (event) => {
  const files = event.target.files;
  if (files.length === 0) return;

  if (!destinationPath) {
    alert("Please select a destination folder first!");
    return;
  }

  const logDiv = document.getElementById("log");
  logDiv.classList.remove("hidden");
  log(`🚀 Starting transfer of ${files.length} files...`);

  try {
    const formData = new FormData();
    for (const file of files) {
      formData.append('files', file);
      log(`📤 Queuing: ${file.name}...`);
    }

    const response = await fetch('/api/transfer-files', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (data.success) {
      log(`✅ Transferred: ${data.transferred} files`);
      if (data.failed > 0) {
        log(`❌ Failed: ${data.failed} files`);
        if (data.results.failed.length > 0) {
          data.results.failed.forEach(f => {
            log(`  - ${f.filename}: ${f.error}`);
          });
        }
      }
      log(`🎉 Done!`);
      alert("Transfer Complete!");
    } else {
      log(`❌ Error: ${data.error}`);
      alert(`Transfer failed: ${data.error}`);
    }
  } catch (err) {
    log(`❌ Error: ${err.message}`);
    alert(`Transfer failed: ${err.message}`);
  }
});

function log(msg) {
  const div = document.getElementById("log");
  div.innerHTML += `<div>${msg}</div>`;
  div.scrollTop = div.scrollHeight;
}
