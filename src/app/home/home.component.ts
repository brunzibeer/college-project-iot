import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Product } from '../settings/product.model';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  products: Product[] = []
  getUrl = "http://ingberna.ddns.net/rfrsh1/app/get-data";

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.onFetchProducts();
  }

  onFetchProducts() {
    this.fetchProducts();
  }

  private fetchProducts() {
    this.http.get<Product[]>(
      this.getUrl)
    .subscribe(prods => {
      this.products = prods;
      console.log(this.products);
    })
  }



}
