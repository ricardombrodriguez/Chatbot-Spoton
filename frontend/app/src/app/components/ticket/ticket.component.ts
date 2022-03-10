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

  
}
