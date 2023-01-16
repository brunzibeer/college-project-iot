export class Product {
    public sens_id: number;
    public name: string;
    public brand: string;
    public asin: string;
    public stock: number;
    public weight: number;
    public value?: number;

    constructor(
        id: number, 
        name: string, 
        brand: string, 
        asin: string, 
        stock: number, 
        weight: number, 
        value: number) {
            
        this.sens_id = id;
        this.name = name;
        this.brand = brand;
        this.asin = asin;
        this.stock = stock;
        this.weight = weight;
        this.value = value;
    }
}