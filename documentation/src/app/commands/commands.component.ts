import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { tap } from 'rxjs';
import { Command } from './command.model';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-commands',
  templateUrl: './commands.component.html',
  styleUrls: ['./commands.component.scss']
})
export class CommandsComponent implements OnInit {
  commands: Command[] = [];
  search = new FormControl('');

  constructor(public http: HttpClient) { }

  ngOnInit(): void {
    this.getCommands();
  }

  getCommands() {
    let headers = new HttpHeaders().set('content-type', 'application/json').set('Access-Control-Allow-Origin', '*')
    this.http.get<Command[]>(
        './assets/commands.json',
        {
            headers: headers
        }
    ).pipe(
        tap(data => JSON.stringify(data))
    ).subscribe(commands => {
      commands = commands.filter(e => e.title.toLowerCase().includes(this.search.value.toLowerCase()) || e.text.toLowerCase().includes(this.search.value.toLowerCase()));
      this.commands = commands;
      for (var i = 0; i < this.commands.length; i++) {
        this.commands[i].id = i;
      }
    })
  }
}
