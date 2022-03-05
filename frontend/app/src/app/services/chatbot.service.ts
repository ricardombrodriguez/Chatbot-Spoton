import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from "@angular/common/http";
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {

  baseUrl = 'http://127.0.0.1:8000/';

  constructor(private http: HttpClient) { }

  sendMessage(message:string): Observable<any> {
    return this.http.get<any>(this.baseUrl + 'message?msg=' + message);
  }

  getAirports(): Observable<any> {
    return this.http.get<any>(this.baseUrl + 'airports');
  }

}
