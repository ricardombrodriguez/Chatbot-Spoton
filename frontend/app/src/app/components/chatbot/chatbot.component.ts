import { Component, Input, OnInit } from '@angular/core';
import { Booking } from 'src/app/classes/booking';
import { Message } from 'src/app/classes/message';
import { ChatbotService } from 'src/app/services/chatbot.service';
import { UserService } from 'src/app/services/user.service';
import { LocationService } from 'src/app/services/location.service';
import { Flight } from 'src/app/classes/flight';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent implements OnInit {

  @Input() message!: string;
  conversations : Message[] = [];
  bookings : Booking[] = [];
  flights : Flight[] = []; 

  startPage!: number;
  paginationLimit!: number;

  public lat:any;
  public lng:any;
  public coords:any;

  constructor(private chatbotService : ChatbotService, private userService : UserService, private locationService: LocationService) { }

  ngOnInit(): void {

    let f1 : Flight = {
      flight_number : "TP2022",
      airline! : "TAP",
      departure! : "03-03-2022",
      dep_airport! : "OPO",
      arr_airport! : "LIS",
      price! : 50
    }

    let f2 : Flight = {
      flight_number : "TP2022",
      airline! : "TAP",
      departure! : "03-03-2022",
      dep_airport! : "OPO",
      arr_airport! : "LIS",
      price! : 100
    }

    this.flights.push(f1)
    this.flights.push(f2)

    // get user message and booking history
    this.getLocation()

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

      //response is a dictionary


      //console.log(response)

      //adicionar mensagem do user à lista de mensagens da conversation
      let botMsg : Message = {msg : response["message"], is_me : false, username : ''+localStorage.getItem('username'), type : response["type"]}
      this.conversations.push(botMsg);

      //console.log(botMsg)
      console.log(botMsg.type)

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

  getLocation() {
    this.locationService.getPosition().then(pos=>
      {
         this.lat = pos.lat
         this.lng = pos.lng
         console.log(`Position: ${this.lat} ${this.lng}`);
    });

    // 
    this.chatbotService.getAirports().subscribe((coords) => {
      this.coords = coords;
    })

    console.log(this.coords)
    
  }


}
