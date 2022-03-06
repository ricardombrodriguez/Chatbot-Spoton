import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from "@angular/common/http";
import { Observable } from 'rxjs';
import { Message } from '../classes/message';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {

  baseUrl = 'http://127.0.0.1:8000/';

  constructor(private http: HttpClient) { }

  sendMessage(message:string): Observable<Message> {
    return this.http.get<Message>(this.baseUrl + 'message?msg=' + message);
  }

}
