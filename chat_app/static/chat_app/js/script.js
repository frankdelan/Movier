document.addEventListener("DOMContentLoaded", function () {

    const messagesContainer = document.querySelector("#chat_log")
    messagesContainer.value = ''
    const messageInput = document.querySelector('[name=message_input]')
    const messageButton = document.querySelector('[name=message_btn]')
    const username = document.querySelector('#username span').innerHTML

    const websocketClient = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/'
        );

    websocketClient.onopen = () => {
        websocketClient.send(JSON.stringify({status: "connect",
                                                    text: `${username} зашел в чат!`,
                                                    username: username}));
        messageButton.onclick = () => {
            websocketClient.send(JSON.stringify({status: "success",
                                        text: messageInput.value,
                                        username: username}));
            messageInput.value = '';
        }
        messageInput.onkeyup = function(e) {
            if (e.key === 'Enter') {
                messageButton.click();
            }
        };
    }

    websocketClient.onerror = (event) => {
        console.error("WebSocket Error:", event);
    };

    websocketClient.onmessage = (message) => {
        let newMessage = JSON.parse(message.data)
        if (newMessage['status'] === 'connect'){
            const welcomeMessage = document.createElement('div')
            welcomeMessage.className = 'welcome'

            welcomeMessage.innerHTML = newMessage['text']
            messagesContainer.appendChild(welcomeMessage)
        }else if (newMessage['status'] === 'disconnect'){
            const byeMessage = document.createElement('div')
            byeMessage.className = 'bye'
            byeMessage.innerHTML = newMessage['text']
            messagesContainer.appendChild(byeMessage)
        }else{
            const userMessage = document.createElement('div')
            userMessage.className = 'message'

            const author = document.createElement('span')
            author.className = 'author';

            const msg = document.createElement('span')
            msg.className = 'msg';

            author.innerHTML = newMessage['username'] + ': '
            msg.innerHTML = newMessage['text']

            userMessage.appendChild(author)
            userMessage.appendChild(msg)
            messagesContainer.appendChild(userMessage)
        }
    }


}, false);