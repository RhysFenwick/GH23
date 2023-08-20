import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UtilsService {
  constructor(private http: HttpClient) {}

  readCSV() {
    return this.http
      .get('../../assets/files/points.csv', { responseType: 'text' })
      .pipe(
        map((data) => {
          console.log(data);
          console.log(typeof data);
          let lines = data.split('\n');
          const headers = lines[0].split(',');
          let csv_data: { [index1: string]: number }[] = [];
          lines.shift();
          return lines;
        })
      );
  }
}
