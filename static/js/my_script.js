/////////////////////////////////// Products /////////////////////////////////////
// حذف پارامترهای خط آدرس
function removeUrlParameter(url, param) {
  // Split the URL into its component parts
  const urlParts = url.split('?');
  
  // Get the path and query string
  const path = urlParts[0];
  const queryString = urlParts[1] || '';
  
    // Remove the parameter from the query string
    const newQueryString = queryString.replace(new RegExp(`${param}=([^&]+)`, 'g'), '');
    
    // Return the new URL
    return `${path}?${newQueryString}`;
  }

// اضافه کردن پارامتر به خط آدرس
function addUrlParameter(url, parameter) {
    // Split the URL into its base and parameters
    url = url.replace(/\?&/g, "?");
    var parts = url.split('?');
    var baseUrl = parts[0];
    var params = {};
    if (parts.length > 1) {
      // Parse the existing parameters into an object
      var paramPairs = parts[1].split('&');
      for (var i = 0; i < paramPairs.length; i++) {
        var pair = paramPairs[i].split('=');
        params[pair[0]] = pair[1];
      }
    }
    // Update or add the new parameter
    var newPair = parameter.split('=');
    params[newPair[0]] = newPair[1];
    // Reconstruct the URL with the updated parameters
    var newParams = [];
    for (var key in params) {
      newParams.push(key + '=' + params[key]);
    }
    var newUrl = baseUrl + '?' + newParams.join('&');
    return newUrl;
  }
// اضافه کردن page به url
function addUrlPageParameter(pageNumber){
  var url = addUrlParameter(window.location.href, "page="+pageNumber);
  window.location = url;
}

// حذف فیلتر قیمت
function remove_price_filter(){
  var url = removeUrlParameter(window.location.href, "&price_max");
  url = removeUrlParameter(url, "price_max");
  url = removeUrlParameter(url, "&price_min");
  url = removeUrlParameter(url, "price_min");
  window.location = url;
}
// حذف فیلتر ویژگی
function remove_feature_filter(){
  var url = removeUrlParameter(window.location.href, "&feature_value");
    url = removeUrlParameter(url, "feature_value");
    window.location = url;
}

// انتخاب مدل مرتب‌سازی محصولات
function select_sort(){
  var select_sort_value = $("#select_sort").val();
  var url = addUrlParameter(window.location.href, "sort_type=" + select_sort_value);
  window.location = url;
}

// انتخاب تعداد محصولات نمایش‌داده‌شده در هر صفحه
// function select_paginate_by(){
  //   var paginate_by = $("#select_paginate_by").val();
  //   var url = addUrlParameter(window.location.href, "paginate_by=" + paginate_by);
//   window.location = url;
// }

// کپی کردن url فعلی در کلیپبورد
function copyToClipboard() {
  var url = window.location.href;
  navigator.clipboard.writeText(url)
    .then(() => {
      alert("لینک اشتراک‌گذاری در کلیپ‌بورد شما کپی شد!");
    })
    .catch((error) => {
      console.error("Failed to copy URL: ", error);
    });
}

// امتیاز دادن به محصول
function addScore(score, productId){
  var starRatings = document.querySelectorAll('.fa-star');

  starRatings.forEach(element => {
    element.classList.remove('checked');
  });

  for (let i = 1; i <= score; i++){
    const element = document.getElementById('star_' + i);
    element.classList.add('checked');
  }

  $.ajax({
    type: 'GET',
    url: '/sides/add_score/',
    data:{
      productId: productId,
      score: score
    },
    success: function(response){
      $("#avg-score").text(response);
    }
  });
  starRatings.forEach(element => {
    element.classList.add('disable');
  });
}


/////////////////////////////////// Orders /////////////////////////////////////

////////////////////// Shop Cart ////////////////////////

shopCartStatus();

function shopCartStatus(){
  $.ajax({
    type: 'GET',
    url: '/orders/shop_cart_status/',
    success: function(response){
      $("#shop_cart_count").text(response);
    }
  });
}

// add
function addToShopCart(product_id, qty){
  if(qty == 0){
    qty = $("#product-quantity").val();
  }
  $.ajax({
    type: 'GET',
    url: '/orders/add_to_shop_cart/',
    data:{
      product_id: product_id,
      qty: qty
    },
    success: function(response){
      shopCartStatus();
    }
  });
}

// delete
function deleteFromShopCart(product_id){
  $.ajax({
    type: 'GET',
    url: '/orders/delete_from_shop_cart/',
    data:{
      product_id: product_id,
    },
    success: function(response){
      shopCartStatus();
      $("#shop_cart_detail").html(response);
    }
  });
}

// update
function updateShopCart(){
  var product_id_list = [];
  var qty_list = [];
  $("input[id^='qty_']").each(function(index){
    product_id_list.push($(this).attr('id').slice(4));
    qty_list.push($(this).val());
  });
  $.ajax({
    type: 'GET',
    url: '/orders/update_shop_cart/',
    data:{
      product_id_list: product_id_list,
      qty_list: qty_list
    },
    success: function(response){
      shopCartStatus();
      $("#shop_cart_detail").html(response);
    }
  });
}

function likeShoppingCart(shopCartButtons){
  shopCartButtons.forEach((shopCartButton) => {
    shopCartButton.className = 'fa fa-shopping-cart shopping-checked';
  });
}

function likeShopCartProducts(productId){
  $.ajax({
    type: 'GET',
    url: '/products/is_at_user_shopcart/',
    data: {productId: productId},
    success: function(response){
      if (response == productId) {
        const shopCartButtons = document.getElementsByName("shopping-cart-"+response);
        likeShoppingCart(shopCartButtons); 
        $('.add_button_'+productId).text('حذف از سبد');
      }else{
        $('.add_button_'+productId).text('افزودن به سبد');
      }
    }
  });
}

function unlikeShoppingCart(shopCartButtons){
  shopCartButtons.forEach((shopCartButton) => {
    shopCartButton.className = 'fa fa-shopping-cart';
  });
  }

function shopCarts(productId){
  const shopCartButtons = document.getElementsByName("shopping-cart-"+productId);

  shopCartButtons.forEach((shopCartButton) => {
    if (shopCartButton.className.includes('shopping-checked')) {

      deleteFromShopCart(productId);
      unlikeShoppingCart(shopCartButtons);
      $('.add_button_'+productId).text('افزودن به سبد');

    } else {

      addToShopCart(productId,1);
      likeShoppingCart(shopCartButtons);
      $('.add_button_'+productId).text('حذف از سبد');
    }
  });

}
/////////////////////////////////// Sides /////////////////////////////////////

////////////////////// Comment ////////////////////////

function showCreateCommentForm(productId, commentId, slug){
  $.ajax({
    type: 'GET',
    url: '/sides/create_comment/' + slug,
    data:{
      productId: productId,
      commentId: commentId
    },
    success: function(response){
      $("#btn_"+commentId).hide();
      $("#comment_form_"+commentId).html(response);
    }
  });
}


////////////////////// Favorite ////////////////////////

favorites_status();

function favorites_status(){
  $.ajax({
    type: 'GET',
    url: '/sides/favorites_status/',
    success: function(response){
      $("#favorites_count").text(response);
    }
  });
}
 
function like(likeButtons){
  likeButtons.forEach((likeButton) => {
    likeButton.className = 'fa fa-heart checked';
  });
}

function likeFavoriteProducts(productId){
  const likeButtons = document.getElementsByName("like-"+productId);

  like(likeButtons);
}

function unlike(likeButtons){
  likeButtons.forEach((likeButton) => {
    likeButton.className = 'fa fa-heart';
  });
  }

function addToFavorites(productId){
  $.ajax({
    type: 'GET',
    url: '/sides/add_to_favorites/',
    data:{
      productId: productId,
    },
    success: function(response){
      favorites_status();
    }
  });
}

function delete_from_favorites(product_id){
  $.ajax({
    type: 'GET',
    url: '/sides/delete_from_favorites/',
    data:{
      product_id: product_id,
    },
    success: function(response){
      favorites_status();
      $("#favorites-detail").html(response);
    }
  });
}

function favorites(productId){
  const likeButtons = document.getElementsByName("like-"+productId);
  // Check the element's class
  likeButtons.forEach((likeButton) => {
    if (likeButton.className.includes('checked')) {
      delete_from_favorites(productId);
      unlike(likeButtons);
    } else {
      addToFavorites(productId);
      like(likeButtons);
    }
  });

}

// function heart_icon(){
//   $.ajax({
//     type: 'GET',
//     url: '/sides/heart_icon/',
//     success: function(response){
//       if (Number(response) == 0){
//         $("#heart_icon").hide();
//       }else{
//         $("#heart_icon").show();
//         $("#favorites_count").text(response);
//       }
//     }
//   });
// }