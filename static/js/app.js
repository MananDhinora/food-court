let openShopping = document.querySelector('.shopping');
let closeShopping = document.querySelector('.closeShopping');
let list = document.querySelector('.list');
let listCard = document.querySelector('.listCard');
let body = document.querySelector('body');
let total = document.querySelector('.total');
let quantity = document.querySelector('.quantity');

openShopping.addEventListener('click', ()=>{
    body.classList.add('active');
})
closeShopping.addEventListener('click', ()=>{
    body.classList.remove('active');
})

let products = [
    {
        id: 1,
        name: 'Veg Double Whopper',
        image: 'veg double whopper.jpeg',
        price: 229
    },
    {
        id: 2,
        name: 'Veg Whopper Cheese',
        image: 'veg whopper with cheese.jpeg',
        price: 204
    },
    {
        id: 3,
        name: 'Mexican Whopper Veg',
        image: 'mexican whopper veg.jpeg',
        price: 220
    },
    {
        id: 4,
        name: 'Veg Whopper Single',
        image: 'veg whopper.jpeg',
        price: 123
    },
    {
        id: 5,
        name: 'Blazing Onion Paprika',
        image: 'Blazing Onion & Paprika.jpeg',
        price: 320
    },
    {
        id: 6,
        name: 'Cheese & Corn Pizza',
        image: 'cheese and corn.jpg',
        price: 120
    },
    {
        id: 7,
        name: 'Farmhouse',
        image: 'Farmhouse.png',
        price: 120
    },
    {
        id: 8,
        name: 'Margherita',
        image: 'margherita.jpg',
        price: 120
    },
    {
        id: 9,
        name: 'Hazelnut Cold Coffee',
        image: 'hazelnut cold coffee.png',
        price: 120
    },
    {
        id: 10,
        name: 'Cappuccino',
        image: 'cappuccino.png',
        price: 120
    },
    {
        id: 11,
        name: 'Hazelnut Hot Chocolate',
        image: 'hazelnut hot chocolate.png',
        price: 120
    },
    {
        id: 12,
        name: 'Hot Chocolate',
        image: 'hot chocolate.png',
        price: 120
    },
    {
        id: 13,
        name: 'Fries',
        image: 'fries.png',
        price: 120
    },
    {
        id: 14,
        name: 'Cheesy Veg Nuggets',
        image: 'cheesy veg nuggets.png',
        price: 120
    },
    {
        id: 15,
        name: 'Salsa Cheesy Fries',
        image: 'salsa cheesy fries.png',
        price: ('₹') + 120 + ('/-')
    },
    {
        id: 16,
        name: 'Veg Pizza Mcpuff',
        image: 'veg pizza Mcpuff.png',
        price: 120
    }

];
let listCards  = [];
function initApp(){
    products.forEach((value, key) =>{
        let newDiv = document.createElement('div');
        newDiv.classList.add('item');
        newDiv.innerHTML = `
            <img src="image/${value.image}">
            <div class="title">${value.name}</div>
            <div class="price">${value.price.toLocaleString()}</div>
            <button onclick="addToCard(${key})">Add To Card</button>`;
        list.appendChild(newDiv);
    })
}
initApp();
function addToCard(key){
    if(listCards[key] == null){
        // copy product form list to list card
        listCards[key] = JSON.parse(JSON.stringify(products[key]));
        listCards[key].quantity = 1;
    }
    reloadCard();
}
function reloadCard(){
    listCard.innerHTML = '';
    let count = 0;
    let totalPrice = 0;
    listCards.forEach((value, key)=>{
        totalPrice = totalPrice + value.price;
        count = count + value.quantity;
        if(value != null){
            let newDiv = document.createElement('li');
            newDiv.innerHTML = `
                <div><img src="image/${value.image}"/></div>
                <div>${value.name}</div>
                <div>${value.price.toLocaleString()}</div>
                <div>
                    <button onclick="changeQuantity(${key}, ${value.quantity - 1})">-</button>
                    <div class="count">${value.quantity}</div>
                    <button onclick="changeQuantity(${key}, ${value.quantity + 1})">+</button>
                </div>`;
                listCard.appendChild(newDiv);
        }
    })
    total.innerText = totalPrice.toLocaleString();
    quantity.innerText = count;
}
function changeQuantity(key, quantity){
    if(quantity == 0){
        delete listCards[key];
    }else{
        listCards[key].quantity = quantity;
        listCards[key].price = quantity * products[key].price;
    }
    reloadCard();
}