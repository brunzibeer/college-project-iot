import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Product } from './product.model';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {
  selectedProduct!: Product;
  infoText = "Please Select a Product"
  showForm = false;
  newProduct: Product = {} as Product;
  postUrl = "http://ingberna.ddns.net/create/app/post-data/new-sens";
  submitted = false;
  word = "New Product"

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  onCreate() {
    this.showForm = !this.showForm;
    if (this.word == "New Product") {
      this.word = "Close Form";
    }
    else {
      this.word = "New Product";
    }
  }

  onSubmit() {
    this.http.post(
      this.postUrl,
      {
        sens_id: this.newProduct.sens_id,
        name: this.newProduct.name,
        brand: this.newProduct.brand,
        asin: this.newProduct.asin,
        stock: this.newProduct.stock,
        weight: this.newProduct.weight,
        value: this.newProduct.value
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
