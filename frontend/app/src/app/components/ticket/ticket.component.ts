import { Component, Input, OnInit } from '@angular/core';
import { Flight } from 'src/app/classes/flight';

import { ChatbotComponent } from '../chatbot/chatbot.component';

@Component({
  selector: 'app-ticket',
  templateUrl: './ticket.component.html',
  styleUrls: ['./ticket.component.css']
})
export class TicketComponent implements OnInit {

  @Input() flight! : Flight;

  constructor(private chatbot :ChatbotComponent) { }

  ngOnInit(): void {
  }

  booking(id: string) {
    this.chatbot.message = "I want book the flight "+ id +"!"
    this.chatbot.sendMessage()
  }
  rating(n: string) {
    if (n=='1'){

      this.chatbot.message = "Rate"
      this.chatbot.sendMessage()
    }else{
      this.chatbot.message = "Bye"
      this.chatbot.sendMessage()
    }
  }
  feedback(n: string) {
    switch (n) {
  
      case '1':
        this.chatbot.message = "1"
        this.chatbot.sendMessage()
        break;
      case '2':
        this.chatbot.message = "2"
        this.chatbot.sendMessage()
          break;
      case '3':
        this.chatbot.message = "3"
        this.chatbot.sendMessage()
        break;
      case '4':
        this.chatbot.message = "4"
        this.chatbot.sendMessage()
        break;
      case '5':
        this.chatbot.message = "5"
        this.chatbot.sendMessage()
        break;
      default:
        break;
    }
  }
}
