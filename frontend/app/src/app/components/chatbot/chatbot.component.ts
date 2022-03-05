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

  sendAutomaticMessage(bttn_id : number) {
    switch(bttn_id) { 
      case 1: { 
        this.sendMessage("No flights right now :/")
        break; 
      } 
      case 2: { 
        this.sendMessage("Paulo faz esse caralho")
        break; 
      } 
      default: { 
        //statements; 
        break; 
      } 
   } 
  }

  sendMessage(message : string) {

    console.log("send message: " + this.message)

    //adicionar mensagem do user à lista de mensagens da conversation
    if (this.message) {
      let userMsg : Message = {msg : this.message, me : true}
      this.conversations.push(userMsg);
    }
    

    console.log("done")

    let botMsg : Message = {msg : message, me : false}
    console.log(botMsg)
    this.conversations.push(botMsg);

    // console.log(this.conversations)

    // this.message = "";

    this.chatbotService.sendMessage(this.message).subscribe((response) => {

      console.log(response)

      //adicionar mensagem do user à lista de mensagens da conversation
      let botMsg : Message = {msg : response, me : false}
      this.conversations.push(botMsg);

      console.log(botMsg)

      // reset do input
      this.message = "";

    })

  }

  showMore() {
    this.paginationLimit = Number(this.paginationLimit) + 3;
  }
  
  showLess() {
    this.paginationLimit = Number(this.paginationLimit) - 3;
  }


}
