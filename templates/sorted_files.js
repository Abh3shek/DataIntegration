document.addEventListener("DOMContentLoaded", function () {
  // Fetch sorted files from the server
  axios
    .get("/sorted_files")
    .then(function (response) {
      // Get the sorted files object from the response
      const sortedFiles = response.data.sorted_files;

      // Get the <ul> element where the sorted files will be appended
      const sortedFileList = document.getElementById("sortedFileList");

      // Iterate over the sorted files object and create <li> elements
      for (const [category, files] of Object.entries(sortedFiles)) {
        const categoryLi = document.createElement("li");
        categoryLi.textContent = category;
        sortedFileList.appendChild(categoryLi);

        const categoryUl = document.createElement("ul");
        for (const file of files) {
          const fileLi = document.createElement("li");
          fileLi.textContent = file;
          categoryUl.appendChild(fileLi);
        }
        sortedFileList.appendChild(categoryUl);
      }
    })
    .catch(function (error) {
      console.error("Error fetching sorted files:", error);
    });
});
