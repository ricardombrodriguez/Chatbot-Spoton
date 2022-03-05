import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Message } from '../classes/message';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  baseUrl = 'http://127.0.0.1:8000/';

  constructor(private http: HttpClient) { }

  sendUsername(): Observable<any> {
    return this.http.get<any>(this.baseUrl + 'identify_user?username=' + sessionStorage.getItem('username'));
  }

  getUserMessages(): Observable<Message[]> {
    return this.http.get<Message[]>(this.baseUrl + 'user_messages?username=' + sessionStorage.getItem('username'));
  }

  getUserBookings(): Observable<any> {
    return this.http.get<any>(this.baseUrl + 'user_bookings?username=' + sessionStorage.getItem('username'));
  }

}
