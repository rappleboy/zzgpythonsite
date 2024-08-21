function publish_article(posturl){
	//编辑图标的父类tr,下面第一个td的text 得到name
	var title = $("#id_title").val(); //由form自动分配的id
	var column_id = $("#which_column").val(); //
	var body = $("#id_body").val();			
	//调用ajax异步提交
	$.ajax({
		url:posturl,
		type:'POST',
		data:{"column_id":column_id,"title":title,"body":body},
		success:function(e){
			if(e=='1'){
				parent.location.reload();
				layer.msg("post successful");
			}else if(e=='2'){
				//db error
				layer.msg("sorry exception");
			}else{
				layer.msg(e);
			}
		},//success 函数
	}); //ajax完了
};//function 完了