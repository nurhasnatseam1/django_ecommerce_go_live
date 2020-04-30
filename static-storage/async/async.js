$(document).ready(function(){
      var productForm=$('.form-product-ajax')
      productForm.submit(function(event){
            event.preventDefault()
            console.log('form submitted but nothing happened')
            var thisForm=$(this)
            var action=thisForm.attr("data-endpoint")
            var httpMethod=thisForm.attr('method')
            var formData =thisForm.serialize()

            $.ajax({
                  url:action,
                  method:httpMethod,
                  data:formData,
                  success:function(data){
                        console.log(data)
                        var submitSpan=thisForm.find('.submit-span')
                        if (data.added){
                              submitSpan.html('In cart<button type="submit" class="btn btn-danger" >remove from  cart</button>')
                        }else{
                              submitSpan.html('In cart<button type="submit" class="btn btn-success" >add to cart</button>')
                        }

                        var currentPath=window.location.href;
                        if(currentPath.indexOf('cart')!= -1){
                              refreshingCart(currentPath)
                        }

                  },
                  error:function(errorData){
                        console.log('error')
                        console.log(errorData)
                  }
            })


            function refreshingCart(currentPath){
                  console.log("refreshing cart")

                  var cartTable=$('.cart-table')
                  var cartBody=cartTable.find('.cart-body')
                  var productRows=cartTable.find('#cart-products')
                  var subtotal=cartBody.find('.subtotal')
                  var total=cartBody.find('.total')

                  


                  var refreshCartUrl='/api/cart/'
                  var refreshCartMethod="GET";
                  var data={};

                  $.ajax({
                        url:refreshCartUrl,
                        method:refreshCartMethod,
                        data:data,
                        success:function(data){
                              console.log(data)
                              if (data.products.length>0){
                                    console.log(productRows)
                                    productRows.html('<tr><td colspan=3 >Comming Soon...</td></tr>')
                                    data.products.forEach(product=>{
                                          productRows.append(

                                                `<tr><th scope="row"></th>
                                                <td><a href="/products/${product.slug}">${product.title}</a>
                                                <form class="form-product-ajax" data-endpoint="{% url 'cart:cart-update' %}" action="{% url 'cart:cart-update' %}" method="POST" class="form">
                                                      <input type="hidden" name="product" value=${product.id}>
                                                      <button type="submit" class="btn btn-link" >Remove</button>
                                                </form>
                                                </td>
                                                <td>${product.price}</td></tr>`
                                                
                                          )
                                    })
                                    productRows.append(
                                    `<tr>
                                          <th colspan="2"></th>
                                          <td> <span class="subtotal">Subtotal:${data.subtotal}</span></td>
                                    </tr>`
                                    )

                                    productRows.append(
                                          `<tr>
                                                <th colspan="2"></th>
                                                <td> <span class="total">total:${data.total}</span></td>
                                          </tr>`
                                          )


                                    productRows.append(
                                          `
                                          <tr>
                                          <th colspan="2"></th>
                                          <td><a href="{% url 'cart:checkout' %}"><button class="btn btn-primary" >Checkout</button></a></td>
                                          </tr>
                                          `
                                    )
 
                              }else{
                                    window.location.href=currentPath
                              }
                        },
                        error:function(data){
                              console.log(error)
                        }
                  })
            }


      })
})