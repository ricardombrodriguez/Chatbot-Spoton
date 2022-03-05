import { Component, Input, OnInit } from '@angular/core';
import { Flight } from 'src/app/classes/flight';

@Component({
  selector: 'app-ticket',
  templateUrl: './ticket.component.html',
  styleUrls: ['./ticket.component.css']
})
export class TicketComponent implements OnInit {

  @Input() flight! : Flight;

  constructor() { }

  ngOnInit(): void {
  }

}
