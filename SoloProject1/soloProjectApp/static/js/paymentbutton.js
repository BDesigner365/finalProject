<div id="paypal-button"></div>
<script src="https://www.paypalobjects.com/api/checkout.js"></script>
<script>
paypal.Button.render({

env: 'sandbox',
client: {
sandbox: 'demo_sandbox_client_id',
production: 'demo_production_client_id'
},

locale: 'en_US',
style: {
size: 'small',
color: 'gold',
shape: 'pill',
},
// Set up a payment
payment: function (data, actions) {
return actions.payment.create({
transactions: [{
amount: {
total: '0.01',
currency: 'USD'
}
}]
});
},
// Execute the payment
onAuthorize: function (data, actions) {
return actions.payment.execute()
.then(function () {
}
window.alert('Thank you for your purchase!');
});
}
}, '#paypal-button');
</script>
