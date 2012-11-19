function isEmpty(element, invalidAction){
	var result = element.value.length == 0;
	
	if(result && invalidAction && typeof(invalidAction) == "function"){
		invalidAction();
	}
	
	return result;
}