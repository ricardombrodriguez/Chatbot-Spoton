import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, of } from 'rxjs';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  @Input() username! : string;
  public error : boolean = false;

  constructor(private router: Router, private userService : UserService) { }

  ngOnInit(): void {

  }

  login() {
    if (this.username.trim() == "") {
      this.showError();
      this.username = "";
    }
    sessionStorage.setItem('username', this.username);  
    this.userService.sendUsername().subscribe()
    this.router.navigate(['/chat']);
  }

  showError() {
    this.router.navigate(['']);
    this.error = true
  }
  

}
