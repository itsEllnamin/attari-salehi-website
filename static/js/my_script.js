/////////////////////////////////// Products /////////////////////////////////////
// حذف پارامترهای خط آدرس
function removeUrlParameter(url, param) {
    // Split the URL into its component parts
    const urlParts = url.split('?');
    
    // Get the path and query string
    const path = urlParts[0];
    const queryString = urlParts[1] || '';
    
    // Remove the parameter from the query string
    const newQueryString = queryString.replace(new RegExp(`${param}=[^&]+`, 'g'), '');
    
    // Return the new URL
    return `${path}?${newQueryString}`;
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