/* Máscaras ER */
function mascara(o,f){
    v_obj=o
    v_fun=f
    setTimeout("execmascara()",1)
}
function execmascara(){
    v_obj.value=v_fun(v_obj.value)
}
function mtel(v){
    console.log("\n\n\n\nOLA cep\n\n\n\n")
    v=v.replace(/\D/g,""); //Remove tudo o que não é dígito
    v=v.replace(/^\d{5}-(\d)/g,"($1) $2"); //Coloca parênteses em volta dos dois primeiros dígitos
    v=v.replace(/(\d)(\d{3})$/,"$1-$2"); //Coloca hífen entre o quarto e o quinto dígitos
    return v;
}
function id( el ){
	return document.getElementById( el );
}
window.onload = function(){
	id('cep').onkeyup = function(){
		mascara( this, mtel );
	}
}