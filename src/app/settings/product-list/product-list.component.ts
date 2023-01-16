import { HttpClient } from '@angular/common/http';
import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { Product } from '../product.model';

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.css']
})
export class ProductListComponent implements OnInit {
  @Output() productWasSelected = new EventEmitter<Product>();
  getUrl = "http://ingberna.ddns.net/rfrsh1/app/get-data";
  products: Product[] = [];

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

  onProductSelected(product: Product) {
    this.productWasSelected.emit(product);
  }

}
