import { Component, Input, OnInit } from '@angular/core';
import { Booking } from 'src/app/classes/booking';
import { Message } from 'src/app/classes/message';
import { ChatbotService } from 'src/app/services/chatbot.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent implements OnInit {

  @Input() message!: string;
  conversations : Message[] = [];
  bookings : Booking[] = [];

  startPage!: number;
  paginationLimit!: number;

  constructor(private chatbotService : ChatbotService, private userService : UserService) { }

  ngOnInit(): void {

    // get user message and booking history

    this.userService.getUserMessages().subscribe((messages) => {
      this.conversations = messages;
      console.log(this.conversations)
    })

    this.userService.getUserBookings().subscribe((bookings) => {
      this.bookings = bookings;
      console.log(this.bookings)
    })

  }

  sendAutomaticMessage(bttn_id : number) {
    switch(bttn_id) { 
      case 1: { 
        this.sendMessage("No flights right now :/")
        break; 
      } 
      case 2: { 
        this.sendMessage("Where you want to travel?")
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
      let userMsg : Message = {msg : this.message, is_me : true, username : ''+localStorage.getItem('username'), type : 'normal'}
      this.conversations.push(userMsg);
    }

    this.chatbotService.sendMessage(this.message).subscribe((response) => {

      console.log(response)

      //adicionar mensagem do user à lista de mensagens da conversation
      let botMsg : Message = {msg : response, is_me : false, username : ''+localStorage.getItem('username'), type : 'normal'}
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
