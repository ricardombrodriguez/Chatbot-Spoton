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
  public carousel_flag: boolean = false;
  public rating_flag: boolean=false;
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

  sendMessage() {

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
      this.rating_flag =false

      //adicionar mensagem do user à lista de mensagens da conversation
      console.log("AQUI "+ response)
      let botMsg!: Message
      if (a_tag == "book"){

      }
      else if (a_tag == "showflights") {

        let all_flights = response['body']['flights']
        let default_msg = response['body']['default_msg']

        this.flights = all_flights;

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

          console.log("flights")
          console.log(this.flights);
        }

      } else {
        let body = response['body']
        botMsg =  {body : body, is_me : false, username : ''+localStorage.getItem('username'), tag : a_tag}
      }

      this.conversations.push(botMsg);
      this.last = this.last + 1 

      // reset do input
      this.message = "";

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
    }) 
  
  }


}
