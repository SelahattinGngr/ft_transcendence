const roomName = JSON.parse(document.getElementById('room-name').textContent)
const user = JSON.parse(document.getElementById('user').textContent)
const conversation = document.getElementById("conversation")
const sendButton = document.getElementById('send')
const inputField = document.getElementById('comment')

const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + roomName + '/')//connection consumer.connect()

conversation.scrollTop = conversation.scrollHeight//sayfa yenilendiğinde mesajların en altta olması için(en güncel mesajların görünmesi için)
//bu fonksiyondan onmessage fonksiyonunda bir tane daha var, o da fonksyion içinde mesaj giderken güncellenmesini ve görünmesini sağlar

// web socketten veri geldğinde çalışır consumer.chat_message()
chatSocket.onmessage=function(e){
    const data = JSON.parse(e.data)

    if (user === data.user){//gelen mesaj bize aitse bu mesaj bloğu çalışır, sağa yazmak için
        var message = `<div class="row message-body">
        <div class="col-sm-12 message-main-sender">
          <div class="sender">
            <div class="message-text">
              ${data.message}
            </div>
            <span class="message-time pull-right">
              ${ data.created_at }
            </span>
          </div>
        </div>
      </div>`
    }
    else{ //gelen mesaj başka bir kullanıcıya aitse bu mesaj bloğu çalışır, sola yazmak için
        var message = `<div class="row message-body">
         <div class="col-sm-12 message-main-receiver">
          <div class="receiver">
            <div class="message-text">
              ${data.message}
            </div>
            <span class="message-time pull-right">
            ${ data.created_at }
            </span>
          </div>
         </div>
      </div>`
    }

    conversation.innerHTML += message//mesajların ekrana (html üzerine) eklenmesi
    conversation.scrollTop = conversation.scrollHeight//mesajlar eklenirken en altta olması için
    
}

chatSocket.onclose = function(e){
    console.error('Chat socket closed unexpectedly');
}

inputField.focus();//direkt mesaj yazma alanına odaklanır

inputField.onkeyup = function(e){
    if(e.keyCode === 13){
        sendButton.click();
    }
}//enter tuşuna basılırsa click çağrılır ve mesaj gönderilir

sendButton.onclick = function(e){
    const message = inputField.value.trim();
    if (message){
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        inputField.value=''
    }
}//mesaj gönderme butonu ile mesaj gönderilir
