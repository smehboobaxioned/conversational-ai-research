// main.js
class ChatWidget extends HTMLElement {
  connectedCallback() {
      this.innerHTML = `<iframe border= 0 width= 100% height= 100% src="https://www.youtube.com/embed/6truGSXOGF4" title="50 Best Classic Music of all time⚜️: Mozart, Tchaikovsky, Vivaldi, Paganini, Chopin" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>`;
  }
}
customElements.define('chat-widget', ChatWidget);

let flag = true;
window.onload = function() {
  // Create the floating icon button
  let floatingIcon = document.createElement('button');
  floatingIcon.id = 'floatingIcon';
  floatingIcon.style.cssText = 'position: fixed; bottom: 100px; right: 100px; background-color: chocolate; cursor: pointer;border-radius: 12px; padding: 15px 32px;';
  floatingIcon.textContent = 'Open Chat';
  document.body.appendChild(floatingIcon);

  // Create the chat widget
  let chatWidget = document.createElement('chat-widget');
  chatWidget.id = 'chatWidget';
  chatWidget.style.display = 'none';
  chatWidget.style.cssText = 'position: fixed; bottom: 150px; right: 120px; width: 300px; height: 500px;';
  document.body.appendChild(chatWidget);

  // Add event listener to the floating icon button
  floatingIcon.addEventListener('click', function() {
      if (flag) {
          chatWidget.style.display = 'block';
          flag = false;
      } else {
          chatWidget.style.display = 'none';
          flag = true;
      }
  });
}