import { Component, Input, OnInit } from '@angular/core';
import { Message } from 'src/app/classes/message';
import { ChatbotService } from 'src/app/services/chatbot.service';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent implements OnInit {

  @Input() message!: string;
  conversations : Message[] = [];

  startPage!: number;
  paginationLimit!: number;

  constructor(private chatbotService : ChatbotService) { }

  ngOnInit(): void {

    // fase de greeting

  }

  sendMessage() {

    console.log("send message: " + this.message)

    //adicionar mensagem do user à lista de mensagens da conversation
    let userMsg : Message = {msg : this.message, me : true}
    this.conversations.push(userMsg);

    console.log("done")

    let botMsg : Message = {msg : "estieidreds", me : false}
    console.log(botMsg)
    this.conversations.push(botMsg);

    console.log(this.conversations)

    this.message = "";

    // mandar mensagem ao backend e receber resposta
    // this.chatbotService.sendMessage(this.message).subscribe((response) => {

    //   //adicionar mensagem do user à lista de mensagens da conversation
    //   let botMsg = new Message(response,false)
    //   this.conversations.push(botMsg);

    //   // reset do input
    //   this.message = "";

    // })

  }

  showMore() {
    this.paginationLimit = Number(this.paginationLimit) + 3;
  }
  
  showLess() {
    this.paginationLimit = Number(this.paginationLimit) - 3;
  }


}
