import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from "@angular/common/http";
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LocationService {

  baseUrl = 'http://127.0.0.1:8000/';

  constructor(private http: HttpClient) { }

  getPosition(): Promise<any> {
    return new Promise((resolve, reject) => {

      navigator.geolocation.getCurrentPosition(resp => {
          resolve({lng: resp.coords.longitude, lat: resp.coords.latitude});
        },
        err =>{
            alert('Error message : '+ err.message);
       });
    });

  }

  getNearestAirport(coords : any): Observable<any> {
    return this.http.get<any>(this.baseUrl + 'nearest_airport?latitude=' + coords['latitude'] + '&longitude=' + coords['longitude']);
  }
}
