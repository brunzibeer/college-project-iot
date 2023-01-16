import { HttpClient } from '@angular/common/http';
import { Component, Input, OnInit } from '@angular/core';
import { Product } from '../product.model';

@Component({
  selector: 'app-product-form',
  templateUrl: './product-form.component.html',
  styleUrls: ['./product-form.component.css']
})
export class ProductFormComponent implements OnInit {
  @Input() product!: Product;
  newProduct: Product = {} as Product;
  postUrl = "http://ingberna.ddns.net/update/app/post-data";
  submitted = false;

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.submitted = false;
  }

  onSubmit() {
    this.http.post(
      this.postUrl,
      {
        sens_id: this.product.sens_id,
        name: this.newProduct.name,
        brand: this.newProduct.brand,
        asin: this.newProduct.asin,
        stock: this.newProduct.stock,
        weight: this.newProduct.weight
      }
    )
    .subscribe(responseData => {
      console.log(responseData);
    })
    this.submitted = true;
  }

  onClear() {
    this.newProduct = {} as Product;
  }

}
