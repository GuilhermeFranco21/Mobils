//Imagem
$('form input[type="file"]').change(event => {
  console.log("kkkkkkkkkkkkkkkkkkk\n kkkkkkkkkk")
  let arquivos = event.target.file;
  if(arquivos.length === 0){
    console.log("Sem imagem para mostrar")
  } else{
    if(arquivos[0].type == 'image/jpeg') {
      $('img').remove();
      let image = $('<img class="img-responsive">');
      Image.attr('src', window.URL.createObjectURL(arquivos[0]));
      $('figure').prepend(imagem);
    } else{
      alert("Formato não suportado")
    }
  }
});

