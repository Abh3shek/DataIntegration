document.addEventListener("DOMContentLoaded", function () {
  // Fetch downloaded files from the server
  axios
    .get("/files")
    .then(function (response) {
      // Get the list of files from the response
      const files = response.data.files;

      // Get the <ul> element where the files will be appended
      const fileList = document.getElementById("fileList");

      // Iterate over the files and create <li> elements
      files.forEach(function (file) {
        const li = document.createElement("li");
        li.textContent = file;
        fileList.appendChild(li);
      });
    })
    .catch(function (error) {
      console.error("Error fetching files:", error);
    });
});
