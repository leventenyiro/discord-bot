import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  openInviteLink() {
    window.open("https://discord.com/oauth2/authorize?client_id=940645443359092806&scope=bot&permissions=8")
  }
}
