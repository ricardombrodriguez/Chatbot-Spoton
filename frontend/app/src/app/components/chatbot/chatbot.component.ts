import { Component, Input, OnInit } from '@angular/core';
import { Booking } from 'src/app/classes/booking';
import { Message } from 'src/app/classes/message';
import { ChatbotService } from 'src/app/services/chatbot.service';
import { UserService } from 'src/app/services/user.service';
import { LocationService } from 'src/app/services/location.service';
import { Flight } from 'src/app/classes/flight';
import { NumberSymbol } from '@angular/common';

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
  current_flight: Flight[] = [];
  rating:string="";
  feedback: string="";

  startPage!: number;
  paginationLimit!: number;

  public lat:any;
  public lng:any;
  public coords:any;
  public carousel_flag: boolean = false;
  public ratings_flag: boolean = false;
  public fb_flag: boolean = false;
  public last: number = 0;

  constructor(private chatbotService : ChatbotService, private userService : UserService, private locationService: LocationService) { }

  ngOnInit(): void {

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
  getLocation() {
    this.locationService.getPosition().then(pos=> {
         this.lat = pos.lat
         this.lng = pos.lng
         this.coords = {'latitude':this.lat,'longitude':this.lng}
         console.log(`Position: ${this.lat} ${this.lng}`);
    });
  }

  getNearbyAirport () {
    this.locationService.getNearestAirport(this.coords).subscribe((response) => {

      let userMsg : Message = {body : 'Get nearest airport from my current location', is_me : true, username : ''+localStorage.getItem('username'), tag : "normal"}
      this.conversations.push(userMsg)

      let botMsg : Message = {body : 'The nearest airport from you is ' + response, is_me : false, username : ''+localStorage.getItem('username'), tag : "normal"}
      this.conversations.push(botMsg)
      console.log(response)
    }) }
  
  sendAutomaticMessage(bttn_id : number) {
    /* switch(bttn_id) { 
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
   } */ 
  }

  sendMessage() {

    this.flights = []

    console.log("send message: " + this.message)

    //adicionar mensagem do user à lista de mensagens da conversation
    if (this.message) {
      let userMsg : Message = {body : this.message, is_me : true, username : ''+localStorage.getItem('username'), tag : 'normal'}
      this.conversations.push(userMsg);
    }

    this.chatbotService.sendMessage(this.message).subscribe((response) => {

      //response is a dictionary
      let a_tag = response['tag']
      this.carousel_flag = false
      this.ratings_flag = false
      this.fb_flag = false
      //adicionar mensagem do user à lista de mensagens da conversation
      console.log("AQUI "+ response)
      let botMsg: Message

      if (a_tag == "showflights") {

        let all_flights = response['body']['flights']
        let default_msg = response['body']['default_msg']
        console.log(all_flights)

        botMsg = {body : default_msg, is_me : false, username : ''+localStorage.getItem('username'), tag : a_tag}

        if (all_flights.length != 0) {

          this.carousel_flag = true

          for (let i = 0; i < all_flights.length; i++) {
            let f = JSON.parse(all_flights[i]);
            console.log(f)
            let new_f : Flight = {
              flight_number : f.flight_iata,
              airline! : f["airline"],
              departure! : f["dep_time"],
              dep_airport! : f["dep_airport"],
              arr_airport! : f["arr_airport"],
              price! : f["price"]
            }
            this.flights.push(new_f)
          }

          this.current_flight = all_flights;

          console.log("flights")
          console.log(this.flights);
        }

      } else if(a_tag == "book"){
        let body = response['body']
 
        this.ratings_flag = true
        botMsg =  {body : body, is_me : false, username : ''+localStorage.getItem('username'), tag : a_tag}

      }else if(a_tag == "feedback"){
        let body = response['body']

        this.fb_flag = true
        botMsg =  {body : body, is_me : false, username : ''+localStorage.getItem('username'), tag : a_tag}

      }else{
        let body = response['body']
        botMsg =  {body : body, is_me : false, username : ''+localStorage.getItem('username'), tag : a_tag}
      }

      console.log(botMsg)


      this.conversations.push(botMsg);
      this.last = this.last + 1 

      //console.log(botMsg)
      console.log(botMsg.tag)

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

  

/*     // 
    this.chatbotService.getAirports().subscribe((coords) => {
      this.coords = coords;
    }) */

    
    
  }


