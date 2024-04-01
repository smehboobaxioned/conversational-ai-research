class ChatWidget extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `<iframe border= 0 width= 100% height= 100% src="https://www.youtube.com/embed/6truGSXOGF4" title="50 Best Classic Music of all time⚜️: Mozart, Tchaikovsky, Vivaldi, Paganini, Chopin" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>`;
  }
}
customElements.define("chat-widget", ChatWidget);

let flag = true;
window.onload = function () {
  // Get the modal
  let modal = document.getElementById("chatModal");
  // Set the modal style dynamically based on the data attribute in HTML
  let { iconbackground = "orange" } = modal.dataset;
  modal.style.cssText = `
    display: none;
    position: fixed;
    z-index: 1;
    left: 20%;
    top: 20%;
    width: 50%;
    height: 60%;
    overflow: auto;
    background-color: green;`;

  // Get the modal content
  let modalContent = document.querySelector("#chatModal .modal-content");
  modalContent.style.cssText = `
  background-color: violet;
  margin: 2% auto;
  border: 1px solid #888;
  width: 80%;
  height: 90%;`;

  // Create the floating icon button
  let floatingIcon = document.createElement("button");
  floatingIcon.id = "floatingIcon";
  floatingIcon.style.cssText = `position: fixed; bottom: 100px; right: 100px; background-color: ${iconbackground}; cursor: pointer;border-radius: 12px; padding: 15px 32px;`;
  floatingIcon.textContent = "Open Chat";
  document.body.appendChild(floatingIcon);

  // Create the chat widget
  let chatWidget = document.createElement("chat-widget");
  chatWidget.id = "chatWidget";

  // Append the chat widget to the modal content
  modalContent.appendChild(chatWidget);

  // Add event listener to the floating icon button
  floatingIcon.addEventListener("click", function () {
    if (flag) {
      modal.style.display = "block";
      document.querySelector("#floatingIcon").textContent = "Close Chat";

      flag = false;
    } else {
      modal.style.display = "none";
      document.querySelector("#floatingIcon").textContent = "Open Chat";
      flag = true;
    }
  });
};
