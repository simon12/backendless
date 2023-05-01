document.addEventListener("DOMContentLoaded", function () {
  const editButtons = document.querySelectorAll(".btn.btn-secondary");
  const deleteButtons = document.querySelectorAll(".btn.btn-danger");

  editButtons.forEach((button) => {
    button.addEventListener("click", handleEdit);
  });

  deleteButtons.forEach((button) => {
    button.addEventListener("click", handleDelete);
  });
});

function handleEdit(event) {
  const testCaseCard = event.target.closest(".card");
  const testCaseName = testCaseCard.querySelector(".card-header").textContent;
  const inputPayload =
    testCaseCard.querySelector("pre:nth-child(2)").textContent;
  const expectedOutput =
    testCaseCard.querySelector("pre:nth-child(4)").textContent;

  const addTestCaseModal = document.getElementById("addTestCaseModal");
  addTestCaseModal.querySelector("#testCaseName").value = testCaseName;
  addTestCaseModal.querySelector("#inputPayload").value = inputPayload;
  addTestCaseModal.querySelector("#expectedOutput").value = expectedOutput;

  addTestCaseModal.addEventListener("hidden.bs.modal", resetTestCaseForm);

  const submitButton = addTestCaseModal.querySelector(".btn.btn-primary");
  submitButton.textContent = "Update Test Case";
  submitButton.removeEventListener("click", submitTestCaseForm);
  submitButton.addEventListener("click", function updateTestCase() {
    submitTestCaseForm("edit");
    submitButton.removeEventListener("click", updateTestCase);
  });
}

function handleDelete(event) {
  if (confirm("Are you sure you want to delete this test case?")) {
    // Delete the test case from the backend
    const testCaseCard = event.target.closest(".card");
    testCaseCard.remove();
  }
}

function submitTestCaseForm(mode = "add") {
  const form = document.getElementById("addTestCaseForm");

  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }

  // Add or update the test case on the backend
  const testCaseName = form.querySelector("#testCaseName").value;
  const inputPayload = form.querySelector("#inputPayload").value;
  const expectedOutput = form.querySelector("#expectedOutput").value;

  if (mode === "add") {
    addTestCase(testCaseName, inputPayload, expectedOutput);
  } else if (mode === "edit") {
    updateTestCase(testCaseName, inputPayload, expectedOutput);
  }

  form.reset();
  const addTestCaseModal = new bootstrap.Modal(
    document.getElementById("addTestCaseModal")
  );
  addTestCaseModal.hide();
}

function addTestCase(name, inputPayload, expectedOutput) {
  const testCases = document.getElementById("testCases");
  const newTestCase = document.createElement("div");
  newTestCase.className = "card mb-3";
  newTestCase.innerHTML = `
    <div class="card-header">Test Case: ${name}</div>
    <div class="card-body">
      <h5 class="card-title">Input Payload</h5>
      <pre>${inputPayload}</pre>
      <h5 class="card-title">Expected Output</h5>
      <pre>${expectedOutput}</pre>
      <div class="text-end">
        <button type="button" class="btn btn-secondary">Edit</button>
        <button type="button" class="btn btn-danger">Delete</button>
      </div>
    </div>
  `;
  testCases.appendChild(newTestCase);

  newTestCase
    .querySelector(".btn.btn-secondary")
    .addEventListener("click", handleEdit);
  newTestCase
    .querySelector(".btn.btn-danger")
    .addEventListener("click", handleDelete);
}

function updateTestCase(name, inputPayload, expectedOutput) {
  const testCaseCard = document
    .querySelector(`div.card-header:contains("Test Case: ${name}")`)
    .closest(".card");

  if (!testCaseCard) {
    console.error("Test case not found. Unable to update.");
    return;
  }

  testCaseCard.querySelector(".card-header").textContent = `Test Case: ${name}`;
  testCaseCard.querySelector("pre:nth-child(2)").textContent = inputPayload;
  testCaseCard.querySelector("pre:nth-child(4)").textContent = expectedOutput;
}

function resetTestCaseForm() {
  const addTestCaseModal = document.getElementById("addTestCaseModal");
  addTestCaseModal.querySelector("#testCaseName").value = "";
  addTestCaseModal.querySelector("#inputPayload").value = "";
  addTestCaseModal.querySelector("#expectedOutput").value = "";

  const submitButton = addTestCaseModal.querySelector(".btn.btn-primary");
  submitButton.textContent = "Save Test Case";
  submitButton.removeEventListener("click", submitTestCaseForm);
  submitButton.addEventListener("click", function () {
    submitTestCaseForm("add");
  });
}

// jQuery selector extension to match text content
$.expr[":"].contains = function (a, i, m) {
  return $(a).text().indexOf(m[3]) >= 0;
};
