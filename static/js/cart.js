var updatebtn = document.getElementsByClassName('update-cart')

for(i=0 ; i<updatebtn.length ; i++){
    updatebtn[i].addEventListener('click', function(){
        var productid = this.dataset.product
        var action = this.dataset.action
        console.log('productid:',productid, 'Action:', action)

        //sconsole.log('USER:',user)
        if (user == 'Anonymeuser'){
            console.log('iser is not authenticated')
        }    
        else{
            updateUserOrder(productid,action)
        }
    })
}

function updateUserOrder(productid,action){
    console.log()
    var url = '/update_item/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content_Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productid':productid, 'action':action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data',data)
        location.reload()
    });
}